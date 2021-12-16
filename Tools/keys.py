# Copyright(c) 2018 STMicroelectronics International N.V.
# Copyright 2017 Linaro Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Copyright (c) 2021 Firmware Modules Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions :
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
#

import os
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from ecdsa import SigningKey, NIST256p, util
import hashlib
from struct import pack
import translate_key_opcode as translate_key
#for AES_CBC lambda pad to 16 bytes by adding the padded value
#(i.e 24 bytes : 0x08 is added  8 times
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * pack("B", 0)

class AES_CBC():
    def __init__(self, key):
        """Construct an AES_CBC private key with the given key data"""
        self.key = key
        self.nonce = []
    @staticmethod
    def generate():
        #use random from platform
        return AES_CBC(os.urandom(16))
    def export_private(self, path):
        if "AES_CBC" not in path:
          print("path does not contains AES_CBC : AES_CBC key should contain AES_CBC string!!!")
          exit(1)
        else:
          with open(path, 'wb') as f:
             f.write(self.key)
    def encrypt(self, payload, nonce=[]):
        if payload == []:
            print("error")
        #Fix me AES CBC is possibly 12 bytes
        if nonce == []:
            nonce = os.urandom(16)
        m = hashlib.sha256()
        print("block size ="+str(AES.block_size))
        encryptor = AES.new(self.key, AES.MODE_CBC, nonce)
        encrypted = ""
        #check if buffer size is aligned on BS size
        if (0 == (len(payload) % BS)):
          # we do not need to pad
          buffer=payload
          encrypted =  encryptor.encrypt(buffer)
        else:
          # Buffer size is not correct (and we do not support ciphertext stealing mode "CBC-CS2" specified in NIST SP 800-38A any more)
          raise Exception("AES CBC encryption requires the Firmware Image size to be a multiple of the AES block size (16 bytes)")
        #compute sh256 on clear buffer without padding
        m.update(payload)
        signature = m.digest()
        #swap the last two block and truncate if required
        return encrypted,signature, nonce
    def trans(self,section, name, end, assembly, version):
        outcode = translate_key.function(section, name,assembly)
        code, bin = translate_key.translate(self.key,end,assembly, version)
        outcode += code
        return outcode
    def trans_bin(self, version):
        code, bin = translate_key.translate(self.key, version=version)
        return bin
    def has_nonce(self):
        return True
    def has_sign(self):
        return False
    def has_encrypt(self):
        return True

class AES_GCM():
    def __init__(self, key):
        """Construct an AES_GCM private key with the given key data"""
        self.key = key
        self.nonce = []
    @staticmethod
    def generate():
        #use random from platform
        return AES_GCM(os.urandom(16))
    def export_private(self, path):
        if "AES_CBC" in path:
          print("path contains AES_CBC : AES_GCM key should not contain AES_CBC!!!")
          exit(1)
        else:
          with open(path, 'wb') as f:
              f.write(self.key)
    def encrypt(self, payload, nonce=[]):
        if payload == []:
            print("error")

        if nonce == []:
            nonce = os.urandom(12)
        encryptor = AES.new(self.key, AES.MODE_GCM, nonce)
        encrypted = encryptor.encrypt(payload)
        signature = encryptor.digest()
        return encrypted,signature, nonce
    def sign(self,payload, nonce):
        encryptor = AES.new(self.key, AES.MODE_GCM, nonce)
        encryptor.update(payload)
        signature =  encryptor.digest()
        return signature, nonce
    def trans(self,section, name, end, assembly, version):
        outcode = translate_key.function(section, name,assembly)
        code, bin = translate_key.translate(self.key,end,assembly, version)
        outcode += code
        return outcode
    def trans_bin(self, version):
        code, bin = translate_key.translate(self.key, version=version)
        return bin
    def has_nonce(self):
        return True
    def has_sign(self):
        return True
    def has_encrypt(self):
        return True


class ECDSA256P1():
    def __init__(self, key):
        """Construct an ECDSA P-256 private key"""
        self.key = key

    @staticmethod
    def generate():
        return ECDSA256P1(SigningKey.generate(curve=NIST256p))

    def export_private(self, path):
        with open(path, 'wb') as f:
            f.write(self.key.to_pem())
    def trans(self,section, name, end, assembly, version):
        vk = self.key.get_verifying_key()
        binarykey = vk.to_string()
        #generate asm code
        outcode = translate_key.function(section, name,assembly)
        code, bin = translate_key.translate(binarykey,end,assembly, version)
        outcode += code
        return outcode
    def trans_bin(self, version):
        vk = self.key.get_verifying_key()
        binarykey = vk.to_string()
        #generate assembled asm code
        code, bin = translate_key.translate(binarykey, version=version)
        #print(code)
        return bin
    def sign(self, payload):
        # To make this fixed length, possibly pad with zeros.
        sig = self.key.sign(payload, hashfunc=hashlib.sha256)
        return sig

    def has_nonce(self):
        return False
    def has_sign(self):
        return True

    def has_encrypt(self):
        return False


def load(path):
    with open(path, 'rb') as f:
        pem = f.read()
    if len(pem) == 16:
        if "AES_CBC" in path:
          return AES_CBC(pem)
        else:
          return AES_GCM(pem)
    else:
        key = SigningKey.from_pem(pem)
        if key.curve.name == 'NIST256p':
            return ECDSA256P1(key)
        else:
            raise Exception("Unsupported")


