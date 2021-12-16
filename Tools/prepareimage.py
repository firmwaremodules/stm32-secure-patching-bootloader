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

import keys
import sys
import argparse
import os
import hashlib
from elftools.elf.elffile import ELFFile
from struct import pack,unpack
from intelhex import IntelHex 

# NOTE: Vector table offset (512 common) must be added to these offsets.

# Offset into bootloader binary, after vector table offset, where the user personalization region begins
# This is consistent across all platforms.
BOOT_USER_PERSO_OFFSET = 0x200

def gen_ecdsa_p256(args):
    keys.ECDSA256P1.generate().export_private(args.key)

def gen_aes_cbc(args):
    keys.AES_CBC.generate().export_private(args.key)

keygens = {
        'aes-cbc': gen_aes_cbc,
        'ecdsa-p256': gen_ecdsa_p256,
        }

def do_keygen(args):
    if args.type not in keygens:
        msg = "Unexpected key type: {}".format(args.type)
        raise argparse.ArgumentTypeError(msg)
    keygens[args.type](args)

def do_trans_bin(args):
    key = keys.load(args.key)
    if args.version=="V6M" or args.version=="V7M": 
        binary = key.trans_bin(args.version)
        # Expected to be called twice, once to write AES privkey and once to write ECC pubkey
        f = open(args.outfile,"ab")
        f.write(binary)
        f.close()
    else:
        print ("-v option : Cortex M architecture not supported")
        exit(1)
def do_getpub(args):
    key = keys.load(args.key)
    key.emit_c()

def do_sha(args):
    payload = []
    with open(args.infile, 'rb') as f:
        payload = f.read()
    m = hashlib.sha256()
    buffer=payload
    m.update(buffer)
    signature = m.digest()
    f = open(args.outfile, "wb")
    f.write(signature)
    f.close()

#########################################################################
## Multisegment support

# Works with GNU toolchains
def get_segmentbinary(elffile,pad=0xff, elftype=0, multi_segaddr=0):
    num = elffile.num_segments()
    binary_offset = 0
    print("elf2segbin number of segment :"+str(num))
    print("elf2segbin looking for multiseg address " + hex(multi_segaddr))
    for i in range(0,num):
        segment= elffile.get_segment(i)
        if segment['p_type'] == 'PT_LOAD':
          if i!=0:
            print(hex(nextaddress))
            if (len(segment.data())):
                segaddr = segment.__getitem__("p_paddr")
                if (multi_segaddr == segaddr):
                    print("elf2segbin found multiseg address " + hex(multi_segaddr))
                    pad_size = 0
                    if (binary_offset != 0):
                        print("fatal: elf2segbin already recorded binary offset!")
                        exit(1)
                    binary_offset = len(binary);
                    print("segment offset " + str(binary_offset))
                else:
                    padd_size=segaddr- nextaddress
                binary+=padd_size*pack("B",pad) 
                binary+=segment.data()
                nextaddress = segaddr + len(segment.data())
          else:
            binary=segment.data()
            if elftype == 0:
              base_address =  segment.__getitem__("p_paddr")
            else:
              base_address , lowest_size =  find_lowest_section(elffile)
              offset = base_address - segment.__getitem__("p_paddr")
              binary = binary[offset:]
            nextaddress = base_address + len(binary)
    return binary, binary_offset

def do_elf2segbin(args):
    with open(args.infile, 'rb') as f:
        my_elffile = ELFFile(f)
        appli_binary, binary_offset = get_segmentbinary(my_elffile, args.value,args.elf,args.segment)
        f.close()

    print("binary size " + str(len(appli_binary)))

    with open(args.outfile, 'wb') as f:
        f.write(appli_binary)
        f.close()

    with open(args.offsetfile, 'wb') as f:
        f.write(pack('I', binary_offset))
        f.close()


#########################################################################


def do_encrypt(args):
    payload = []
    with open(args.infile, 'rb') as f:
        payload = f.read()
        f.close()
        
        if args.padding > 0 and len(payload) % args.padding != 0:
            padding = args.padding - (len(payload) % args.padding)
            print("padding " + str(len(payload)) + " with " + str(padding) + " byte: " + str(args.padbyte))
            payload += padding * pack("B",args.padbyte)

    key = keys.load(args.key) if args.key else None
    if key.has_encrypt():
        if key.has_nonce():
            nonce = []
            if args.nonce and args.iv:
                print("either IV or Nonce Required for this key!!!")
                exit(1)
            if args.nonce:
                iv_nonce=args.nonce
            elif args.iv:
                iv_nonce=args.iv
            else:
                print("either IV or Nonce Required for this key!!!")
                exit(1)
            if os.path.isfile(iv_nonce):
                with open(iv_nonce, 'rb') as f:
                    nonce = f.read()
            encrypted , signature , nonce_used = key.encrypt(payload, nonce)
            if nonce !=nonce_used:
                f = open(iv_nonce, 'wb')
                f.write(nonce_used)
                f.close()
        else:
            encrypted ,signature = key.encrypt(payload)

        f=open(args.outfile,"wb")
        f.write(encrypted)
        f.close()
    else:
        print("Key does not support encrypt")
        exit(1)

def do_header_lib(args):
    if (os.path.isfile(args.firmware)):
        size = os.path.getsize(args.firmware)
    else:
        print("no fw file")
        exit(1)
    if os.path.isfile(args.tag):
        f=open(args.tag, 'rb')
        tag = f.read()
    key = keys.load(args.key) if args.key else None
    nonce = b''
    protocol = args.protocol
    magic = args.magic.encode()
    version = args.version
    reserved = b'\0'*args.reserved
    if args.segmentfile and os.path.isfile(args.segmentfile):
        f=open(args.segmentfile, 'rb')
        reserved = f.read()
        args.reserved = 4
    if args.nonce and args.iv:
        print("either IV or Nonce Required !!!")
        exit(1)
    iv_nonce=""
    if args.nonce:
        iv_nonce=args.nonce
    elif args.iv:
        iv_nonce=args.iv
    if iv_nonce:
        with open(iv_nonce, 'rb') as f:
            nonce = f.read()

    header = pack('<'+str(len(magic))+'sH'+str(len(nonce))+'s'+'II'+str(len(tag))+'s'+str(args.reserved)+'s',
                    magic, protocol, nonce, version, size, tag, reserved)
    if key.has_sign():
        if key.has_nonce() and iv_nonce=="":
            print("sign key required nonce, provide nonce")
            exit(1)
        if key.has_nonce():
            if nonce != b'':
                signature , nonce_used = key.sign(header, nonce)
                if nonce_used !=nonce:
                    print("error nonce used differs")
                    exit(1)
            else:
                print("nonce required for this key")
                exit(1)
        else:
            signature = key.sign(header)
        header +=pack(str(len(signature))+'s',signature)
    else:
        print("Provided Key is not useable to sign header")
        exit(1)
    return header, signature

#header is used only to build install header for merge .elf tool
def do_header(args):
    header ,signature  = do_header_lib(args)
    f=open(args.outfile,"wb")
    if len(signature) == 16:
        signature = 2*signature
    elif len(signature) == 64:
        signature = signature[0:32]
    else:
        print("Unexpected signature size : "+str(len(signature))+"!!")
    f.write(header)
    f.write(signature)
    f.write(signature)
    f.write(signature)
    padding = args.offset - (len(header)+ 3*32)
    while (padding != 0):
        f.write(b'\xff')
        padding = padding - 1
    f.close()

def do_pack(args):
    header,signature = do_header_lib(args)
    f=open(args.outfile,"wb")
    f.write(header)
    if len(header) > args.offset:
        print("error header is larger than offset before binary")
        sys.exit(1)

    tmp = (args.offset-len(header))*b'\xff'
    f.write(tmp)
    binary=open(args.firmware,'rb')
    tmp=binary.read()
    f.write(tmp)
    binary.close()

def do_packpatch(args):
    args.segmentfile = None
    patchheader,patchsignature = do_header_lib(args)
    toheaderfile=open(args.header, 'rb')
    toheader=toheaderfile.read()
    toheadertrunc=toheader[:128]
    f=open(args.outfile,"wb")
    f.write(patchheader)
    f.write(toheadertrunc)
    binary=open(args.encpatch,'rb')
    tmp=binary.read()
    f.write(tmp)
    binary.close()

def find_lowest_section(elffile):
     lowest_addr = 0
     lowest_size = 0
     for s in elffile.iter_sections():
        sh_addr =  s.header['sh_addr'];
        if sh_addr !=0:
            if lowest_addr == 0:
                lowest_addr = sh_addr
            elif sh_addr < lowest_addr:
                lowest_addr = sh_addr
                lowest_size = s.header['sh_size']
     return lowest_addr, lowest_size

#return base address of segment, and a binary array,
#add padding pattern
def get_binary(elffile,pad=0xff, elftype=0):
    num = elffile.num_segments()
    print("number of segment :"+str(num))
    for i in range(0,num):
        segment= elffile.get_segment(i)
        if segment['p_type'] == 'PT_LOAD':
          if i!=0:
            print(hex(nextaddress))
            if (len(segment.data())):
                padd_size=segment.__getitem__("p_paddr")- nextaddress
                binary+=padd_size*pack("B",pad) 
                binary+=segment.data()
                nextaddress = segment.__getitem__("p_paddr") + len(segment.data())
          else:
            binary=segment.data()
            if elftype == 0:
              base_address =  segment.__getitem__("p_paddr")
            else:
              base_address , lowest_size =  find_lowest_section(elffile)
              offset = base_address - segment.__getitem__("p_paddr")
              binary = binary[offset:]
            nextaddress = base_address + len(binary)
    return binary, base_address

# bin file merge: combine the bootloader, application and header components into a .bin file
def do_merge(args):
    with open(args.infile, 'rb') as f:
        my_elffile = ELFFile(f)
        appli_binary, appli_base = get_binary(my_elffile, args.value,args.elf)
    with open(args.sbsfu, 'rb') as f:
        if args.baseaddr:
            boot_binary = bytearray(f.read())
            f.close()
            boot_base = args.baseaddr
        else:
            my_elffile = ELFFile(f)
            boot_binary, boot_base = get_binary(my_elffile, args.value, args.elf)
            boot_binary = bytearray(boot_binary)
    with open(args.install, 'rb') as f:
        header_binary = f.read()
    
    if args.keyfile:
        with open(args.keyfile, 'rb') as f:
            VECTOR_TABLE_OFFSET=0x200
            if args.offset:
                VECTOR_TABLE_OFFSET=args.offset
            keybytes = bytearray(f.read())
            f.close()
            boot_binary[VECTOR_TABLE_OFFSET+BOOT_USER_PERSO_OFFSET:VECTOR_TABLE_OFFSET+BOOT_USER_PERSO_OFFSET+len(keybytes)] = keybytes
            print("inserted " + str(len(keybytes)) + " key bytes at offset " + hex(VECTOR_TABLE_OFFSET+BOOT_USER_PERSO_OFFSET))

    address_just_after_sbsfu = len(boot_binary)+boot_base
    beginaddress_header = appli_base - len(header_binary)
    if (beginaddress_header >= address_just_after_sbsfu):
        print("Merging")
        print("BOOT Base = "+hex(boot_base))
        print("Writing header = "+hex(beginaddress_header))
        print("APP Base = "+hex(appli_base))
        padd_before_header =   beginaddress_header - address_just_after_sbsfu
        big_binary = boot_binary + padd_before_header * pack("B",args.value) + header_binary + appli_binary
            
    else:
        print("(mergebin) sbsfu is too large to merge with appli !! base offset=" + hex(beginaddress_header) + " < sizeof sbsfu=" + hex(address_just_after_sbsfu))
        exit(1)
    print("Writing to "+str(args.outfile)+" "+str(len(big_binary)))
    with open(args.outfile, 'wb') as f:
        f.write(big_binary)

#Find segments in the elf and add them to an intelhex object
#at each segments offset.  Return the intelhex object
def get_hex(elffile,pad=0xff, elftype=0):
    ih = IntelHex()
    num = elffile.num_segments()
    print("get_hex number of segment :"+str(num))
    for i in range(0,num):
        segment= elffile.get_segment(i)
        if segment['p_type'] == 'PT_LOAD':
          if i!=0:
            if (len(segment.data())):
                address = segment.__getitem__("p_paddr")
                print("get_hex: segment " + hex(address))
                ih.frombytes(segment.data(), offset=address)
          else:
            binary=segment.data()
            if elftype == 0:
              base_address =  segment.__getitem__("p_paddr")
            else:
              base_address , lowest_size =  find_lowest_section(elffile)
              offset = base_address - segment.__getitem__("p_paddr")
              binary = binary[offset:]

            print("get_hex: segment " + hex(base_address))
            ih.frombytes(binary, offset=base_address)

    return ih, base_address

# hex file merge: combine the BOOT, application and header components into a .hex file
def do_mergehex(args):
    with open(args.infile, 'rb') as f:
        my_elffile = ELFFile(f)
        appli_hex, appli_base = get_hex(my_elffile, args.value,args.elf)
    with open(args.sbsfu, 'rb') as f:
        if args.baseaddr:
            boot_binary = f.read()
            f.close()
            boot_base = args.baseaddr
        else:
            my_elffile = ELFFile(f)
            boot_hex, boot_base = get_hex(my_elffile, args.value, args.elf)
            boot_binary, boot_base = get_binary(my_elffile, args.value, args.elf)
    with open(args.install, 'rb') as f:
        header_binary = f.read()
        f.close()

    ih = IntelHex()

    address_just_after_sbsfu = len(boot_binary)+boot_base
    beginaddress_header = appli_base - len(header_binary)
    if (beginaddress_header >= address_just_after_sbsfu):
        print("Merging")
        print("BOOT Base = "+hex(boot_base))
        print("Writing header = "+hex(beginaddress_header))
        print("APP Base = "+hex(appli_base))
        
        ih.loadbin(args.install, offset = beginaddress_header)

        if args.baseaddr:
            ih.loadbin(args.sbsfu, offset = boot_base)
        else:
            ih.merge(boot_hex)

        if args.keyfile:
            VECTOR_TABLE_OFFSET=0x200
            if args.offset:
                VECTOR_TABLE_OFFSET=args.offset
            ih.loadbin(args.keyfile, offset = boot_base + VECTOR_TABLE_OFFSET+BOOT_USER_PERSO_OFFSET)
            print("inserted key bytes at offset " + hex(VECTOR_TABLE_OFFSET+BOOT_USER_PERSO_OFFSET))

        ih.merge(appli_hex)

    else:
        print("(mergehex) sbsfu is too large to merge with appli !! base offset=" + hex(beginaddress_header) + " < sizeof sbsfu=" + hex(address_just_after_sbsfu))
        exit(1)
    print("Writing to "+str(args.outfile))
    ih.tofile(args.outfile, format='hex')

subcmds = {
        'keygen': do_keygen,
        'transbin':do_trans_bin,
        'getpub': do_getpub,
        #hash a file with sha256 and provide result in in a file
        'sha256': do_sha,
        # convert an elf file to bin file, with the special feature of eliminating the
        # fill before the specified segment address.  That is, the elf file is converted
        # normally to a binary file *except* at the jump to the specified segment address.
        # In addition, the offset into the generated binary file where this occurs
        # is stored in a temporary file.
        #   segment address required, -o
        #   file to write offset in file, -f
        #   elf file (in)
        #   bin file (out)
        'elf2segbin' : do_elf2segbin,
        #encrypt binary file with provided key
        # -k -n
        'enc': do_encrypt,
        # give what to put  in header and provide the key to compute hmac
        # magic (2 bytes) required, -m
        # protocol version(2 bytes) required , -p
        # nonce optional , -n
        # fwversion (required) 2 bytes, -ver
        # fw file (to get the size)
        # fw tag  (file)
        # reserved size
        # key
        # offset default 512
        'header':do_header,
        # give what to pack a single file header
        # magic (2 bytes) required, -m
        # protocol version(2 bytes) required , -p
        # nonce optional , -n
        # fwversion (required) 2 bytes, -ver
        # fw file (to get the size)
        # fw tag  (file)
        # reserved size
        # key
        # offset default 512
        #
        'pack':do_pack,
        # give what to pack a single patch file header
        # magic (2 bytes) required, -m
        # protocol version(2 bytes) required , -p
        # nonce optional , -n
        # fwfromversion (required) **OF FROM FIRMWARE** 2 bytes, -ver 
        # fw file (to get the size)
        # fw tag  (file)
        # reserved size
        # key
        # pre-generated header of full image (this contains the TO version)
        # (optional) segment file containing segment offsets discovered in elf2segbin in binary
        'packpatch':do_packpatch,
        #merge appli.elf , header binary and sbsfu elf or bin in a big binary
        #input file appli.elf
        #-h header file
        #-s sbsfu.elf or sbsfu.bin (requires -b arg)
        #output file binary to merge
        #-v byte pattern to fill between the different segment default 0xff
        #-p padding length to add to appli binary
        #-b baseaddr base address in flash of BOOT binary supplied with -s.
        'merge':do_merge,
        #merge appli.elf , header binary and sbsfu elf in a hex file
        #input file appli.elf
        #-h header file
        #-s sbsfu.elf or sbsfu.bin (requires -b arg)
        #output file hex to merge
        #-v byte pattern to fill between the different segment default 0xff (not used but retained for compatibility with merge command)
        #-b baseaddr base address in flash of BOOT binary supplied with -s.
        'mergehex':do_mergehex
        }

def auto_int(x):
    return int(x, 0)

def args():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(help='subcommand help', dest='subcmd')
    keygenp = subs.add_parser('keygen', help='Generate pub/private keypair')
    keygenp.add_argument('-k', '--key', metavar='filename', required=True)
    keygenp.add_argument('-t', '--type', metavar='type',
            choices=['ecdsa-p256','aes-cbc'],
            required=True)

    transbin =  subs.add_parser('transbin', help='translate key to pre-assembled execute only code')
    transbin.add_argument('-k', '--key', metavar='filename', required=True)
    transbin.add_argument('-v', '--version',help='fix CORTEX M architecture', type=str,required = False, default="V7M")   
    transbin.add_argument('outfile')

    getpub = subs.add_parser('getpub', help='Get public key from keypair')
    getpub.add_argument('-k', '--key', metavar='filename', required=True)

    sha = subs.add_parser('sha256', help='hash a file with sha256')
    sha.add_argument("infile")
    sha.add_argument("outfile")
    sha.add_argument('-p', '--padding',type=int, required = False, default=0, help='pad to be a multiple of the given size if needed')

    elf2segbin = subs.add_parser('elf2segbin', help='convert and elf to a bin file with segment detection')
    elf2segbin.add_argument('-s', '--segment', required = True, type=auto_int, default=0x0)
    elf2segbin.add_argument('-o', '--offsetfile', metavar='filename', required = True)
    elf2segbin.add_argument('-e', '--elf', help='elf type set to 1 for GNU, 0 for other by default', type=int, default=1) 
    elf2segbin.add_argument('-v', '--value', help= "byte padding pattern", required = False, type=int, default=0xff)
    elf2segbin.add_argument("infile")
    elf2segbin.add_argument("outfile")

    enc = subs.add_parser('enc', help='encrypt an image with a private key')
    enc.add_argument('-k', '--key', metavar='filename', required = True)
    enc.add_argument('-n', '--nonce', metavar='filename')
    enc.add_argument('-i', '--iv', metavar='filename')
    enc.add_argument('-p', '--padding',type=int, required = False, default=0, help='pad to be a multiple of the given size if needed')
    enc.add_argument('-b', '--padbyte', type=int, default=0, help='byte to use as padding if needed')
    enc.add_argument("infile")
    enc.add_argument("outfile")

    head = subs.add_parser('header', help='build  installed header file and compute mac according to provided key')
    head.add_argument('-k', '--key', metavar='filename', required = True)
    head.add_argument('-n', '--nonce', metavar='filename')
    head.add_argument('-i', '--iv', metavar='filename')
    head.add_argument('-f', '--firmware', metavar='filename', required = True)
    head.add_argument('-t', '--tag', metavar='filename', required = True)
    head.add_argument('-v', '--version',type=int, required = True)
    head.add_argument('-m', '--magic',type=str,  default="SU", help='SFUMagic must be 2 characters')
    head.add_argument('-p', '--protocol',type=int,  default = 0x1)
    head.add_argument('-r', '--reserved',type=int, default=8)
    head.add_argument('-o', '--offset', type=int, default = 512, required = False)
    head.add_argument('-s', '--segmentfile', metavar='filename')
    head.add_argument("outfile")
    
    pack = subs.add_parser('pack', help='build header file and compute mac according to key provided')
    pack.add_argument('-k', '--key', metavar='filename', required = True)
    pack.add_argument('-n', '--nonce', metavar='filename')
    pack.add_argument('-i', '--iv', metavar='filename')
    pack.add_argument('-f', '--firmware', metavar='filename', required = True)
    pack.add_argument('-t', '--tag', metavar='filename', required = True)
    pack.add_argument('-v', '--version',type=int, required = True)
    pack.add_argument('-m', '--magic',type=str,  default="SU", help='SFUMagic must be 2 characters')
    pack.add_argument('-p', '--protocol',type=int, default = 0x1)
    pack.add_argument('-r', '--reserved',type=int, default=8)
    pack.add_argument('-o', '--offset', help='offset between start of header and binary', type=int, default=512)
    pack.add_argument('-e', '--elf', help='elf type set to 1 for GNU, 0 for other by default', type=int, default=1) 
    pack.add_argument('-s', '--segmentfile', metavar='filename')
    pack.add_argument("outfile")

    packpatch = subs.add_parser('packpatch', help='build signed and encrypted patch file (sfbp) for distribution')
    packpatch.add_argument('-k', '--key', metavar='filename', required = True)
    packpatch.add_argument('-n', '--nonce', metavar='filename')
    packpatch.add_argument('-i', '--iv', metavar='filename')
    packpatch.add_argument('--encpatch', metavar='filename', required=True, help='encrypted patch for inclusion')
    packpatch.add_argument('-f', '--firmware', metavar='filename', required = True, help='raw patch for obtaining length')
    packpatch.add_argument('-t', '--tag', metavar='filename', required = True)
    packpatch.add_argument('-v', '--version',type=int, required = True)
    packpatch.add_argument('-m', '--magic',type=str, default="SU", help='SFUMagic must be 2 characters')
    packpatch.add_argument('-p', '--protocol',type=int, default = 0x11)
    packpatch.add_argument('-r', '--reserved',type=int, default=8)
    packpatch.add_argument('--header', help='pre-generated header of full firmware (what the patch will create)', metavar='toheader', required = True)
    packpatch.add_argument("outfile")

    mrg = subs.add_parser('merge', help='merge elf appli , install header and sbsfu.elf in a contiguous binary')
    mrg.add_argument('-i', '--install', metavar='filename',  help="filename of installed binary header", required = True)
    mrg.add_argument('-s', '--sbsfu', metavar='filename', help="filename of sbsfu elf or bin (requires -b if bin)", required = True)
    mrg.add_argument('-v', '--value', help= "byte padding pattern", required = False, type=int, default=0xff)
    mrg.add_argument('-p', '--padding', help='pad to add to appli binary, a multiple of the given size if needed',type=int, required = False, default=0)
    mrg.add_argument('-e', '--elf', help='elf type set to 1 for GNU, 0 for other by default', type=int, default=1) 
    mrg.add_argument('-b', '--baseaddr', help='base address of BOOT if bin file is supplied, otherwise extracted from elf.', type=lambda x: int(x,0), required = False)
    mrg.add_argument('-k', '--keyfile', metavar='filename', help='boot keys file')
    mrg.add_argument('-o', '--offset', help='offset / size of vector table', type=int, default=512)
    mrg.add_argument("infile", help="filename of appli elf file" )
    mrg.add_argument("outfile", help = "filename of contiguous binary")

    mrghex = subs.add_parser('mergehex', help='merge elf appli , install header and sbsfu.elf or bin in a hex file')
    mrghex.add_argument('-i', '--install', metavar='filename',  help="filename of installed binary header", required = True)
    mrghex.add_argument('-s', '--sbsfu', metavar='filename', help="filename of sbsfu elf or bin (requires -b if bin)", required = True)
    mrghex.add_argument('-v', '--value', help= "byte padding pattern", required = False, type=int, default=0xff)
    mrghex.add_argument('-e', '--elf', help='elf type set to 1 for GNU, 0 for other by default', type=int, default=1) 
    mrghex.add_argument('-b', '--baseaddr', help='base address of BOOT if bin file is supplied, otherwise extracted from elf.', type=lambda x: int(x,0), required = False)
    mrghex.add_argument('-k', '--keyfile', metavar='filename', help='boot keys file')
    mrghex.add_argument('-o', '--offset', help='offset / size of vector table', type=int, default=512)
    mrghex.add_argument("infile", help="filename of appli elf file" )
    mrghex.add_argument("outfile", help = "filename of hex")

    args = parser.parse_args()
    if args.subcmd is None:
        print('Must specify a subcommand')
        sys.exit(1)
    subcmds[args.subcmd](args)

if __name__ == '__main__':
    args()

