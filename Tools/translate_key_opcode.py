# Copyright(c) 2018 STMicroelectronics International N.V.
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

import os
from array import array
from struct import pack


def reglistR1(endreg):
    # Fill bits in reglist bitfield, excluding R0, R1 up to endreg
    return (((1 << (endreg + 1)) - 1) & 0xfffe)

def opSTMR0v7(bin, endreg):
    # STM.W Rn,<registers>
    # 1110 1000 1000 nnnn 000r rrrr rrrr rrrr
    # Note we MUST NOT USE WRITEBACK (!) because R0 is incremented by a subsequent ADDS instruction
    opcode = 0xE8800000 | reglistR1(endreg)
    appendOpcode32(bin, opcode)   



def opSTMR0v6(bin, endreg):
    # STM R0!, {R1, Rendreg }
    # 11000 000 xxxxxxx0   <--- 8 bits, each bit sets a register to copy, R0-R7
    # Note in thumb T1, writeback (!) is always set/true, so R0! is not required.
    opcode = 0xC000 | reglistR1(endreg)
    appendOpcode16(bin, opcode)
    

def opPUSHR1R5(bin):
    # PUSH {R1, R5}
    # 1011 0 10 0 xxxxxxx0
    opcode = 0xB400 | reglistR1(5)
    appendOpcode16(bin, opcode)

def opPOPR1R5(bin):
    # POP {R1, R5}
    # 1011 1 10 0 xxxxxxx0
    opcode = 0xBC00 | reglistR1(5)
    appendOpcode16(bin, opcode)

def opBXLR(bin):
    # BX LR  (R14)
    # 010001 11 0 xxxx 000  - > 0100 0111 0111 0000
    opcode = 0x4770
    appendOpcode16(bin, opcode)


def opADDR0v6(bin, imm):
    # ADDS R0, R0, #imm
    # 001 10 000 xxxxxxxx
    opcode = 0x3000 | (imm & 0xFF)
    appendOpcode16(bin, opcode)

def opADDR0v7(bin, imm):
    # ADDS.W R0, R0, #imm
    # Encoding T3 to match output of GCC assembler for "ADD R0, R0, #16".
    opcode = 0xF1000000 | (imm & 0xFF)
    appendOpcode32(bin, opcode)

def opADDSv6(bin, Rd, Rn, Rm):
    # ADDS Rd, Rn, Rm   T1
    # 000 11 00 mmm nnn ddd  -> 0001 100m mmnn nddd
    opcode = 0x1800
    opcode |= ((Rd & 0x7) << 0)
    opcode |= ((Rn & 0x7) << 3)
    opcode |= ((Rm & 0x7) << 6)
    appendOpcode16(bin, opcode)

def opADDv6(bin, Rd, Rm):
    # ADDS Rdn, Rm  (Rd = Rn)  T2
    # 010001 000 mmmm ddd  -> 0100 0100 0mmm mddd
    opcode = 0x4400
    opcode |= ((Rd & 0x7) << 0)
    opcode |= ((Rm & 0xf) << 3)
    appendOpcode16(bin, opcode)

def opMOVSv6(bin, destreg, imm):
    # MOVS Rd, #imm8
    # 001 00 ddd xxxxxxxx
    opcode = 0x2000
    opcode |= ((destreg & 0x7) << 8)
    opcode |= (imm & 0xff) 
    appendOpcode16(bin, opcode)

def opLSLSv6(bin, destreg, imm):
    # LSLS Rd, Rm, #imm5  (Rd = Rm)
    # 000 00 xxxxx mmm ddd
    opcode = 0x0000
    opcode |= ((destreg & 0x7) << 3)
    opcode |= ((destreg & 0x7) << 0)
    opcode |= ((imm & 0x1f) << 6)
    appendOpcode16(bin, opcode)

def opMOVIMMv7(imm):
    # MOVX Rd, #imm16
    # 11110 x 100100 xxxx 0 xxx dddd xxxxxxxx -> 1111 0x10 0100 xxxx 0xxx dddd xxxxxxxx
    #                                                  xxxxxxxxxxxxxxxx................
    #                                                          xxxxxxxxxxxxxxxx........
    #                                                            xxxxxxxxxxxxxxxx......
    opcode = 0
    opcode |= ((imm & 0xF000) << 4)  # imm4  top 4 bits moved up 4 bits to land at [3-0] in upper word
    opcode |= ((imm & 0x0800) << 15) # i  bit 11 moved up into bit 10 of upper word
    opcode |= ((imm & 0x0700) << 4)  # imm3 [10-8] moved up to bits [14-12] of lower word
    opcode |= ((imm & 0x00FF) << 0)  # imm8 [7-0] copied straight over to [7-0] of lower word
    return opcode

def opMOVWv7(bin, destreg, imm):
    # MOVW Rd, #imm16
    # 11110 x 100100 xxxx 0 xxx dddd xxxxxxxx -> 1111 0x10 0100 xxxx 0xxx dddd xxxxxxxx
    opcode = 0xF2400000
    opcode |= ((destreg & 0xf) << 8) 
    opcode |= opMOVIMMv7(imm)
    appendOpcode32(bin, opcode)

    
def opMOVTv7(bin, destreg, imm):
    # MOVT Rd, #imm16
    # 11110 x 101100 xxxx 0 xxx dddd xxxxxxxx -> 1111 0x10 1100 xxxx 0xxx dddd xxxxxxxx
    #                                                  xxxxxxxxxxxxxxxx................
    #                                                          xxxxxxxxxxxxxxxx........
    #                                                            xxxxxxxxxxxxxxxx......
    opcode = 0xF2C00000
    opcode |= ((destreg & 0xf) << 8) 
    opcode |= opMOVIMMv7(imm)
    appendOpcode32(bin, opcode)

def appendOpcode16(bin, opcode):
    bin += pack('<H', opcode)

def appendOpcode32(bin, opcode):
    bin += pack('<H', (opcode >> 16) & 0xffff)
    bin += pack('<H', opcode & 0xffff)

#generating execute only code function for ARMV7M
#based on :
# 0xABCD
#    MOVW Rn, #0xBA
#    MOVT Rn  #0xCD
# AREA KEY, CODE
# EXPORT ReadKey
# 16 bytes AEG_GCM key
#PUSH {R4, R7}
# 32 bytes (pub_x, pub_y)
#PUSH {R4, R11}
def build_mov(reg, val, version, bin):
    if version == "V7M":
        #build the 2 16bits to write
        out ="\tMOVW R"+str(reg)+", #"+hex(val[1]*256+val[0])+"\n"
        opMOVWv7(bin, reg, val[1]*256+val[0])
        out +="\tMOVT R"+str(reg)+", #"+hex(val[3]*256+val[2])+"\n"
        opMOVTv7(bin, reg, val[3]*256+val[2])
    elif version == "V6M":    
        out ="\tMOVS R"+str(reg)+", #"+hex(val[3])+"\n"
        opMOVSv6(bin, reg, val[3])
        out +="\tLSLS R"+str(reg)+", R"+str(reg)+", #24\n"
        opLSLSv6(bin, reg, 24)
        out +="\tMOVS R5, #"+hex(val[2])+"\n"
        opMOVSv6(bin, 5, val[2])
        out +="\tLSLS R5, R5, #16\n"
        opLSLSv6(bin, 5, 16)
        out +="\tADD R"+str(reg)+", R"+str(reg)+", R5\n"
        opADDv6(bin, reg, 5)
        out +="\tMOVS R5, #"+hex(val[1])+"\n"
        opMOVSv6(bin, 5, val[1])
        out +="\tLSLS R5, R5, #8\n"
        opLSLSv6(bin, 5, 8)
        out +="\tADD R"+str(reg)+", R"+str(reg)+", R5\n"
        opADDv6(bin, reg, 5)
        out +="\tMOVS R5, #"+hex(val[0])+"\n"
        opMOVSv6(bin, 5, val[0])
        out +="\tADD R"+str(reg)+", R"+str(reg)+", R5\n"
        opADDv6(bin, reg, 5)
    else:
        exit(1)    
    return out

def translate(key, end=False, assembly="IAR", version="V7M"):
    if version == "V7M":        
        STMR0 = "\tSTM R0"
        ADDR0 = "\tADD R0"
        opSTMR0 = opSTMR0v7
    elif version == "V6M":    
        STMR0 = "\tSTM R0!"
        opSTMR0 = opSTMR0v6
    else:
        exit(1)

    binary = bytearray([])
    key=bytearray(key)
    if len(key) <= 16:
        endreg = int((len(key)+3)/4)
        loop = 1
    elif len(key) == 32:
        endreg = int(4)
        loop = 2
    elif len(key) == 64:
        endreg = int(4)
        loop = 4
    else:
        return ""
    output = "\tPUSH {R1-R5}\n"
    opPUSHR1R5(binary)
    for j in range(0,loop):
        if j!=0:
            output+= STMR0 +", {R1-R"+str(endreg)+"}\n"
            opSTMR0(binary, endreg)
            if version == "V7M":
                output+= ADDR0 +", R0,#16\n"
                opADDR0v7(binary, 16)
        for i in range(0,endreg):     
            output+=build_mov(i+1, key[16*j+i*4:16*j+i*4+4], version, binary)
    output += STMR0 + ", {R1-R"+str(endreg)+"}\n"
    opSTMR0(binary, endreg)
    output += "\tPOP {R1-R5}\n"
    opPOPR1R5(binary)
    output += "\tBX LR\n"
    opBXLR(binary)
    if end:
        if assembly == "GNU":
            output +="\t.end"
        else:
            output +="\tEND"
    return output, binary

def function(section, name, assembly="IAR" ):
    if assembly == "IAR":
      section_name="section "
      separator=":CODE\n"
    elif assembly == "ARM":
      section_name="AREA |"
      separator="|, CODE\n"
    elif assembly == "GNU":
      section_name=".section "
      separator=""","a",%progbits\n .syntax unified \n .thumb \n
      """
    else:
      exit(1)
    if section !="":
        out = "\t"+str(section_name)+str(section)+str(separator)
    else:
        out=""
    if assembly == "GNU":
        out += "\t.global "+str(name)+"\n"
        out += str(name)+":\n"
    else:
        out += "\tEXPORT "+str(name)+"\n"
        out += str(name)+"\n"
    return out
if __name__ == '__main__':
    assembly = "GNU"
    binary = bytearray([])
    outcode = function(".SE_Key_Data", "SE_ReadKey", assembly=assembly)
    key="OEM_KEY_COMPANY1".encode()
    code, bin = translate(key, assembly=assembly, version="V6M")
    outcode += code
    binary += bin
    key = bytearray([0xce, 0x40, 0x14, 0xc6, 0x88, 0x11, 0xf9, 0xa2, 0x1a, 0x1f, 0xdb, 0x2c, 0x0e,
    0x61, 0x13, 0xe0, 0x6d, 0xb7, 0xca, 0x93, 0xb7, 0x40, 0x4e, 0x78, 0xdc, 0x7c,
    0xcd, 0x5c, 0xa8, 0x9a, 0x4c, 0xa9])
    outcode += function("", "SE_ReadKey_PubY", assembly=assembly)
    code, bin = translate(key, assembly=assembly, version="V6M")
    outcode += code
    binary += bin
    outcode += function("", "SE_ReadKey_PubX", assembly=assembly)
    key = bytearray([ 0x1c, 0xcb, 0xe9, 0x1c, 0x07, 0x5f, 0xc7, 0xf4, 0xf0, 0x33, 0xbf, 0xa2, 0x48,
    0xdb, 0x8f, 0xcc, 0xd3, 0x56, 0x5d, 0xe9, 0x4b, 0xbf, 0xb1, 0x2f, 0x3c, 0x59,
    0xff, 0x46, 0xc2, 0x71, 0xbf, 0x83])

    code, bin = translate(key, assembly=assembly, version="V6M")
    outcode += code
    binary += bin
    if assembly == "GNU":
      outcode +="\t.end"
    else:
      outcode +="\tEND"
    print(outcode)
    print(str(key))
    print(bytes(binary).hex(' '))
    print(len(binary))

    binary = bytearray([])
    outcode = function(".SE_Key_Data", "SE_ReadKey", assembly=assembly)
    key="OEM_KEY_COMPANY1".encode()
    code, bin = translate(key, assembly=assembly, version="V7M")
    outcode += code
    binary += bin
    outcode += function("", "SE_ReadKey_PubY", assembly=assembly)
    code, bin = translate(key, assembly=assembly, version="V7M")
    outcode += code
    binary += bin
    outcode += function("", "SE_ReadKey_PubX", assembly=assembly)
    code, bin = translate(key, assembly=assembly, version="V7M")
    outcode += code
    binary += bin
    if assembly == "GNU":
      outcode +="\t.end"
    else:
      outcode +="\tEND"
    print(outcode)
    print(str(key))
    print(bytes(binary).hex(' '))
    print(len(binary))



