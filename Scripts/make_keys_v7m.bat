@echo off

echo %0 : Generate new secure keys for stm32-secure-patching-bootloader and Cortex-M3/M4/M7 (V7M and later) architecture devices

set _KEY_TOOL=..\Tools\prepareimage.py
set _OUTPUT_DIR=%1

if [%_OUTPUT_DIR%]==[] (
    echo Please specify destination path to application Keys directory
    goto:eof
)

if NOT EXIST %_KEY_TOOL% (
    echo Key generation tool is not found %_KEY_TOOL%
    goto:eof
)


set _CIPHER_KEY=Cipher_Key_AES_CBC.bin
set _SIGNING_KEY=Signing_PrivKey_ECC.txt
set _MACHINE_FILE=machine.txt

echo Making %_OUTPUT_DIR%/%_CIPHER_KEY%
python %_KEY_TOOL% keygen -k %_OUTPUT_DIR%\%_CIPHER_KEY% -t aes-cbc

echo Making %_OUTPUT_DIR%/%_SIGNING_KEY%
python %_KEY_TOOL% keygen -k %_OUTPUT_DIR%\%_SIGNING_KEY% -t ecdsa-p256

echo Making %_OUTPUT_DIR%/%_MACHINE_FILE%
echo V7M > %_OUTPUT_DIR%/%_MACHINE_FILE%

