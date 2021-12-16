#!/bin/bash - 

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



# Arguments:
#
#  arg1 - Name of application input .elf file  example: "${BuildArtifactFileBaseName}.elf"
#  arg2 - Keys directory relative to build directory.  example:  "../../Keys"
#  arg3 - Binary directory relative to build directory.  example: "../../../../../Binary"
#  arg4 - Build version (0 or 0.0.0 for auto version)
#  arg5 - Patch reference version (if not found, no patch generated)
#  arg6 - Board name (e.g. NUCLEO-L073RZ)
#  arg7 - Bootloader version (e.g. 1.0.0)
#  arg8 - Vector table offset from the slot base for the platform (e.g. 512) Cannot be 0.
#  arg9   Multisegment address (e.g. 0x90000000 if used, or 0 if not used)

# If you are following the project structure outlined in the demonstration application:
#
# Postbuild command is "../../../../../../../Bootloader/Scripts/STM32CubeIDE/postbuild.sh" "${BuildArtifactFileBaseName}" "../../Keys" "../../../../../Binary" "1.0.0" "1.0.0" "NUCLEO-L073RZ" "1.0.0" 512 0
#                                                                                                                                                               Build   Patch    Board          BootVer Vect MultiSeg          
#
#  arg2 is "../../Keys"
#  arg3 is "../../../../../Binary"
#
#    |- Project\
#    |    |- Binary\
#         |- DemoApp\
#              | - <Target>\
#                     | - STM32CubeIDE\
#                             |- <Project>_<Target>\    (STM32CubeIDE project folder .project .cproject)
#                             |         | - <BuildDir>\ (e.g. Debug)
#                             | - Keys\
#                           

ApplicationName=$1
BuildVer=$4
PatchRefVer=$5
BoardName=$6
BootVer=$7
VectOffset=$8
MultiSegAddr=$9

# Setup references to the stm32-secure-patching-bootloader inputs
# Path to *this* script is derived from the name.
# This points to the Script dir
ScriptDir=$(realpath $(dirname "$0"))
# We need reference to the Tools dir
ToolsDir=$(realpath $ScriptDir/../../Tools)
# We need reference to the Libs dir
LibsDir=$(realpath $ScriptDir/../../Libs)

# Setup references to the application project inputs and outputs
BuildDir=`pwd`
# We need reference to the project's Keys dir
KeysDir=$(realpath $BuildDir/$2)
# We need reference to the output products directory
BinaryDir=$(realpath $BuildDir/$3)

OutputDump=$BuildDir/output.txt

echo "Running postbuild"
echo "Running postbuild" >> $OutputDump

elf=${ApplicationName}.elf
bin=${ApplicationName}.bin

if [ ! -e $ToolsDir ]; then
    echo "FATAL: ToolsDir "$ToolsDir" is not found."
    exit 1
fi
if [ ! -e $LibsDir ]; then
    echo "FATAL: LibsDir "$LibsDir" is not found."
    exit 1
fi
if [ ! -e $KeysDir ]; then
    echo "FATAL: KeysDir "$KeysDir" is not found."
    exit 1
fi
if [ ! -e $BinaryDir ]; then
    echo "FATAL: BinaryDir "$BinaryDir" is not found."
    exit 1
fi
if [ $VectOffset == 0 ]; then
    echo "FATAL: VectOffset is not defined."
    exit 1
fi
if [ -z ${BootVer+x} ]; then
    echo "FATAL: BootVer is not defined."
    exit 1
fi
if [ -z ${BoardName+x} ]; then
    echo "FATAL: BoardName is not defined."
    exit 1
fi

echo Using:
echo - $ScriptDir
echo - $ToolsDir
echo - $LibsDir
echo - $BuildDir
echo - $KeysDir
echo - $BinaryDir
echo - $OutputDump
echo - $ApplicationName
echo - $BuildVer
echo - $PatchRefVer
echo - $BoardName
echo - $BootVer
echo - $VectOffset
echo - $MultiSegAddr

#-----------------------------------------------------------------------------------

# Versioning: 
#  We are deriving the version automatically from the Git build environment.
#  We have to create a 3-digit major.minor.build version from this, so it
#  is paramount that the repository has a proper Git tag committed at some
#  time in the past.  Without a proper tag, the version can only be parsed into 0.0.0.
#  The 3-digit build number is embedded into the firmware image
#  headers for the bootloader and patch engine to use to detect version mismatches, etc.
#
#  This is how it works:
#  Version from Git is 'git describe --tags --always --dirty' and reports, for example:
#    v1.2.3-12-g1a2b3c4
#  This tag is "v1.2.3" and has 12 commits since.  The 12 is added to the build number to
#  create the final 3-digit version: 1.2.15.  In the case the build is from an immediate tag,
#  the tag simply becomes the 3-digit version.  Released builds should always be built from an immediate tag.
#
#  For patch generation, we need to know the "from version" on which to base the patch.
#  This is passed in as the 3-digit version that has been appended to a file that exists
#  in the Binary/PatchRef directory.  For example, the IDE's postbuild command line
#  has "v1.1.2" as BuildVer.  Then this script finds "PatchRef/DemoApp_v1.1.2.bin" to use as the
#  reference firmware.  The new patch file would be "DemoApp_v1.1.2_v1.2.15.sfbp" and can only
#  be applied to devices that is currently running v1.1.2 firmware.  Please note if you
#  tag "v1.2.3" use that as BuildVer, and if you tag "1.2.3" use that as arg 4.  The parser
#  will find the 3-digit version from either format, and the file names always get the "BuildVer" string
#  whether that was set in the postbuild arguments or obtained from git.
#
#  Lastly, please note that the 32-bit version field in the firmware image header can support
#  major: 0-255, minor: 0-65535 and build: 0-255.


#
# Inputs:
#  $1 - Output of 'git describe --tags --always --dirty'
#
# Returns:
#   VERSION_NUMBER : single 32-bit value representing the major.minor.patch extracted from the input.
#   VERSION_DIGITS : "major.minor.patch" extracted from the input.
#
#   0 on success, 1 on error.

extract_version_number() {

  #echo "extract_version_number: $1"
  if [ -n "$1" ]; then
    # Confirm a 3-digit version number is present
    digitstring=`expr $1 : 'v*\([0-9]*\.[0-9]*\.[0-9]*\)'`
    #echo "string: $digitstring"

    if [ -n "$digitstring" ]; then
      # Find the components
      MAJOR=`expr $digitstring : '\([0-9]*\)\.[0-9]*\.[0-9]*'`
      MINOR=`expr $digitstring : '[0-9]*\.\([0-9]*\)\.[0-9]*'`
      PATCH=`expr $digitstring : '[0-9]*\.[0-9]*\.\([0-9]*\)'`
      VERSION_DIGITS="$MAJOR.$MINOR.$PATCH"
      #echo "version digits=$VERSION_DIGITS"
      # Check if there is a commit number component
      commitstring=`expr $1 : '.*-\([0-9]*\)-'`
      if [ -n "$commitstring" ]; then
        #echo "commit: $commitstring"
        PATCH=$((PATCH + $((commitstring))))
        #echo $PATCH
      fi
      MAJOR=$((MAJOR & 0xFF))
      MINOR=$((MINOR & 0xFFFF))
      PATCH=$((PATCH & 0xFF))
      VERSION_NUMBER=$(($((MAJOR << 24)) + $((MINOR << 8)) + $((PATCH)))) 
      #echo "Version number=$VERSION_NUMBER"
      return 0
                 
    fi
  fi

  # error
  VERSION_DIGITS="0.0.0"
  VERSION_NUMBER=0
  echo "Error finding version for input $1" >> $OutputDump 
  return 1

}

# In auto-version mode, BuildVer is just "0" or "0.0.0" or "v0.0.0" and we use the output of
# 'git describe --tags --always --dirty'
# See if we are in auto mode and if so, get the version.  
# NOTE! if no tag exists with a parse-able vX.Y.Z or X.Y.Z semantic version scheme,
#  the generated firmware image header will have a version of 0.0.0 which is probably not what you want.
#  In other words, don't use auto-version mode unless you are explicitly tagging your release builds (git tag v1.0.0; git push --tags)'
#  It is OK to have intermediate builds after a tag: e.g. v1.0.0-12--g302ab62 will generate firmware header with version 1.0.0.
extract_version_number $BuildVer
if [ $VERSION_NUMBER == 0 ]; then
    echo "Auto version mode"
    BuildVer=`git describe --tags --always --dirty`
fi

echo "Using version=$BuildVer from $PatchRefVer" 
# Create new output.txt
echo "Using version=$BuildVer from $PatchRefVer" > $OutputDump

# Get the "to" version number
extract_version_number $BuildVer
version=$BuildVer
version_number=$VERSION_NUMBER
echo "version digits=$VERSION_DIGITS, number=$VERSION_NUMBER" >> $OutputDump

# Get the "from" version number
extract_version_number $PatchRefVer
fromversion=$PatchRefVer
fromversion_number=$VERSION_NUMBER
echo "From version digits=$VERSION_DIGITS, number=$VERSION_NUMBER" >> $OutputDump

# $version and $fromversion must include 'v' if required
execname=${ApplicationName}_${version}
patchrefname=${ApplicationName}_${fromversion}
patchname=${ApplicationName}_${fromversion}_${version}

#-----------------------------------------------------------------------------------


PatchRefDir=$BinaryDir"/PatchRef"

# Setup names of various outputs
rawbin=$PatchRefDir"/"$execname".bin"
patchrefbin=$PatchRefDir"/"$patchrefname".bin"
patchbin=$PatchRefDir"/"$patchname".patch"
sfu=$BinaryDir"/"$execname".sfu"
sfup=$BinaryDir"/"$patchname".sfup"
sfb=$BinaryDir"/"$execname".sfb"
sfbp=$BinaryDir"/"$patchname".sfbp"
sign=$BinaryDir"/"$execname".sign"
signpatch=$BinaryDir"/"$patchname".sign"
headerbin=$BinaryDir"/"$execname"sfuh.bin"
bigbinary=$BinaryDir"/BOOT_"$execname".bin"
bighex=$BinaryDir"/BOOT_"$execname".hex"
segoff=$BinaryDir"/"$execname".segoff"

iv=$KeysDir"/iv.bin" 
oemkey=$KeysDir"/Cipher_Key_AES_CBC.bin"
ecckey=$KeysDir"/Signing_PrivKey_ECC.txt"
# Machine type is specified by file on a per-project basis
machine_type_file=$KeysDir"/machine.txt"
# This bin file is written to this script directory for injection into the bootloader binary 
# user personalization section.
keyfile=$KeysDir/boot_keys.bin

# Get target machine type (v6m or v7m) - needed to know how to generate the key material.
if [ -e "$machine_type_file" ]; then  
  machine_type=`cat $machine_type_file`
  echo "machine type is "$machine_type
  echo "machine type is "$machine_type >> $OutputDump
else
  echo "machine type file "$machine_type_file" is missing!"
  echo "machine type file "$machine_type_file" is missing!" >> $OutputDump
fi

# We must remove the IV file, if it exists, because we want a new, unique and random
# encryption IV generated and placed into each signed header.  If the IV file exists, it is used,
# otherwise the image tool stores the one generated and used by the encryption algorithm.
# It is essential that the IV is used only once for each encryption to maintain the
# strength of the AES CBC algorithm.
if [ -e  "$iv" ]; then
  rm  $iv
fi

# FW image processing tool
prepareimage=$ToolsDir/prepareimage.py
cmd=python

echo "$cmd $prepareimage" >> $OutputDump
# Make sure we have a Binary sub-folder for outputs
if [ ! -e $BinaryDir ]; then
  mkdir $BinaryDir
fi

# Make sure we have a PatchRef sub-folder in Binary folder
if [ ! -e $PatchRefDir ]; then
  mkdir $PatchRefDir
fi

# Set the patch difference tool
patchtool=$ToolsDir"/jdiff.exe"

# Setup reference to the stm32-secure-patching-bootloader binary we are going to use.
Stm32BootBinName="stm32-secure-patching-bootloader_"$BoardName"_"$BootVer".bin"
bootbin=$LibsDir/$BoardName/$Stm32BootBinName
echo "Using "$Stm32BootBinName
echo "Using "$bootbin >> $OutputDump

# Ensure the assembled key file is not present before generating (it is opened for append)
if [ -e "$keyfile" ]; then
    rm $keyfile
fi
# Generate the assembled key file
command=$cmd" "$prepareimage" transbin -k "$oemkey" -v "$machine_type" "$keyfile
$command >> $OutputDump
ret=$?
if [ $ret == 0 ]; then
    command=$cmd" "$prepareimage" transbin -k "$ecckey" -v "$machine_type" "$keyfile
    $command >> $OutputDump
    ret=$?
fi
if [ $ret != 0 ]; then
  msg="Error creating bootloader keys file: "$keyfile
  echo $msg
  exit 1
fi

# ***********************************************************************************
# Preparation of the binary file is required before we can process it.
# In the standard flow, the binary file is already produced by the toolchain.
# However, to support multiple segments, the binary must be "compressed" to eliminate the filler
# in the gaps between segments, especially if the segment is in completely different memory
# region (e.g. QSPI 0x90000000).  For both regular and multi-segment flows, we use our own
# elf to binary file converter.  This will overwrite anything the toolchain may have produced.
# all we need is the ELF for any firmware production flow.
command=$cmd" "$prepareimage" elf2segbin -e 1 -v 255 -s "$MultiSegAddr" -o "$segoff" "$elf" "$bin
$command >> $OutputDump
ret=$?
if [ $ret != 0 ]; then
  msg="Error creating bin file from elf file."
  echo $msg
  exit 1
fi

# ***********************************************************************************
# Create signed header and merged production image of new firmware.
#  Here we:
#    1. Compute the unencrypted firmware binary hash (sha256), output %sign%
#    2. Create the header using hash and firmware length, output %headerbin%
#    3. Create the merged image, e.g. BOOT_DemoApp_BOARD_vX.Y.Z, output %bighex%, and %bigbinary% if segment offset is 0.
#
#  The patch file uses the generated header in its processing steps.
# ***********************************************************************************
command=$cmd" "$prepareimage" enc -k "$oemkey" -i "$iv" "$bin" "$sfu
$command >> $OutputDump
ret=$?
if [ $ret == 0 ]; then
  command=$cmd" "$prepareimage" sha256 "$bin" "$sign
  $command >> $OutputDump
  ret=$?
  if [ $ret == 0 ]; then 
    command=$cmd" "$prepareimage" pack -k "$ecckey" -r 4 -v "$version_number" -i "$iv" -s "$segoff" -f "$sfu" -t "$sign" "$sfb" -o "$VectOffset
    $command >> $OutputDump
    echo Made $sfb
    ret=$?
    if [ $ret == 0 ]; then
      command=$cmd" "$prepareimage" header -k  "$ecckey" -r 4 -v "$version_number"  -i "$iv" -s "$segoff" -f "$sfu" -t "$sign" -o "$VectOffset" "$headerbin
      $command >> $OutputDump
      ret=$?
      if [ $ret == 0 ]; then
        # Create a combined hex file, which can handle multiple segments.  This is the default format.
        command=$cmd" "$prepareimage" mergehex -v 255 -e 1 -i "$headerbin" -s "$bootbin" -b 0x08000000 -k "$keyfile" -o "$VectOffset" "$elf" "$bighex
        $command >> $OutputDump
        echo Made $bighex
        if [ $MultiSegAddr == 0 ]; then
          # If the segment offset is 0 (disabled) we can also create a combined binary.
          # Use the pre-built bootloader binary for this.  All supported targets start flash at 0x08000000.
          command=$cmd" "$prepareimage" merge -v 0 -e 1 -i "$headerbin" -s "$bootbin" -b 0x08000000 -k "$keyfile" -o "$VectOffset" "$elf" "$bigbinary
          $command >> $OutputDump
          echo Made $bigbinary
        fi

        ret=$?

        # ***********************************************************************************
        # Create firmware update patch
        # 
        # First, copy the generated raw application binary to the patch reference directory
        # to serve as a potential source for a future patch update.
        if [ $ret == 0 ]; then
          command="cp "$bin" "$rawbin
          $command >> $OutputDump
          ret=$?
          # If the selected "from" version  exists and versions aren't equal perform patch generation
          if [ -e $patchrefbin ]; then
            if [ ! $version_number == $fromversion_number ]; then
              # Create the patch file between the specified reference version and this version
              command=$patchtool" "$patchrefbin" "$rawbin" "$patchbin
              $command >> $OutputDump
              # Error here can be set if there is no difference between files.
              ret=$?
              if [ $ret == 0 ]; then
                command=$cmd" "$prepareimage" enc -k "$oemkey" -i "$iv" -p 16 "$patchbin" "$sfup
                $command >> $OutputDump
                ret=$?
                if [ $ret == 0 ]; then
                  command=$cmd" "$prepareimage" sha256 "$patchrefbin" "$signpatch
                  $command >> $OutputDump
                  ret=$?
                  if [ $ret == 0 ]; then
                    command=$cmd" "$prepareimage" packpatch -k "$ecckey"  -r 4 -v "${fromversion_number}" -i "$iv" -f "$patchbin" --encpatch "$sfup" -t "$signpatch" --header "$headerbin" "$sfbp
                    $command >> $OutputDump
                    echo Made $sfbp
                    ret=$?
                  fi
                fi
              else
                echo "Error running patch difference tool: No differences detected." >> $OutputDump
              fi
            else
              echo "FROM version same as new version, skipping patch generation. ["$patchrefbin"]" >> $OutputDump
            fi
          else
            echo "FROM version file not found, skipping patch generation. ["$patchrefbin"]" >> $OutputDump
          fi
        fi
      fi
    fi
  fi
fi

if [ $ret == 0 ]; then
  rm $sign
  rm $sfu
  rm $headerbin
  if [ -e "$segoff" ]; then
    rm $segoff
  fi
  if [ -e "$signpatch" ]; then
    rm $signpatch
  fi
  if [ -e "$sfup" ]; then
    rm $sfup
  fi
  if [ -e "$keyfile" ]; then
    rm $keyfile
  fi
  if [ -e  "$iv" ]; then
    rm  $iv
  fi
  echo "Postbuild finished."
  exit 0
else 
  echo "$command : failed" >> $OutputDump
  if [ -e  "$elf" ]; then
    rm  $elf
  fi
  if [ -e "$elfbackup" ]; then 
    rm  $elfbackup
  fi
  echo $command : failed
  read -n 1 -s
  exit 1
fi
