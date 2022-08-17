## DISCO-L4R9I

"Multisegment" feature is enabled, so there is a small test string located at the start
of the OSPI external flash that is part of the application binary.  This string is updated to show
"version 2" instead of "version 1" in the provided test update files.  

### Expected output after programming `BOOT_TestApp_XXXX.hex|.bin`

**Please note: Ensure that the appropriate DISCO-L4R9I External Flash Loader is selected in STM32CubeProgrammer before progamming the .hex file.**

```
[  0.000] Bootloader starting up.
STM32 Secure Patching Bootloader. github.com/firmwaremodules/stm32-secure-patching-bootloader
Build: v1.3.0-preview1
Registered to: unregistered
Target: DISCO-L4R9I
UID: 0450474d7e346720
Clock:MSI,40,120,HSI48 Crypto:SW UART:2,115200,N81
SLOT0:08015000 SLOT1:90400000 SIZE:5EB000
APP RAMSTART:20001700 VTOR:08015200
[  0.030] Target check: CPUID:410FC241 IDCODE:10036470 FLASHSZ:0800 .. OK.
[  0.106] OSPI init success.
[  0.363] Verify bootloader.
[  0.414] SHA256: ab740a57991159b68a734ed9d4282d6756018c82a09c7fa4ab5ced499ee3a371 Valid
[  0.422] UART loader check trigger.
[  1.428] Check USB flash media.
[  2.430] No valid firmware found on flash media, status=1
[  2.436] Verify slot 1 header.
[  2.439] Slot 1 is empty.
[  2.441] Verify slot 0.
[  2.444] Verify slot 0 header.
[  2.648] Verify slot 0 signature.
[  2.670] Verify slot 0 ready.
[  2.673] Verify slot 0 fw ver.
[  2.878] Slot 0 has valid active firmware version 1.3.0
[  2.883] Preparing to launch application in slot 0.

TestApp starting...


======================================================================
=                                                                    =
=        stm32-secure-patching-bootloader Test Application           =
=                                                                    =
======================================================================
  Board: DISCO-L4R9I (32L4R9IDISCOVERY)
  FW Version: 1.3.0
  FW Build: v1.3.0-preview1
  FW Tag: 0x05C76A5C
  OSPI External Flash string: This is a version 1 message from OSPI External Flash!
  Version 1


=================== Main Menu ============================

  Update Firmware (.sfb or .sfbp) over YMODEM ----------- 1

  Test Bootloader API ----------------------------------- 2


================ Call Bootloader APIs =========================

Firmware Info:
        Active FW Version: 16777984 (1.3.0)
        Active FW Size: 30464 bytes
        Active FW Tag: 05C76A5C064304DF276BD5FD04EE7B772039F0510F9DBDA1C34D5B08853F7841
Bootloader Version:
        v1.3.0-preview1

```

### Expected output after YMODEM transfer of `TestApp_XXXX_vYYYY_vZZZZ.sfbp` (patch file)

```
================ YMODEM Firmware Updater =========================

  -- Send Firmware

  -- -- File> Transfer> YMODEM> Send .

  -- -- Programming Completed Successfully! (1)

  -- -- Bytes: 560

  -- Image correctly downloaded (status=0) - reboot


[  0.000] Bootloader starting up.
STM32 Secure Patching Bootloader. github.com/firmwaremodules/stm32-secure-patching-bootloader
Build: v1.3.0-preview1
Registered to: unregistered
Target: DISCO-L4R9I
UID: 0450474d7e346720
Clock:MSI,40,120,HSI48 Crypto:SW UART:2,115200,N81
SLOT0:08015000 SLOT1:90400000 SIZE:5EB000
APP RAMSTART:20001700 VTOR:08015200
[  0.030] Target check: CPUID:410FC241 IDCODE:10036470 FLASHSZ:0800 .. OK.
[  0.106] OSPI init success.
[  0.363] Verify bootloader.
[  0.414] SHA256: ab740a57991159b68a734ed9d4282d6756018c82a09c7fa4ab5ced499ee3a371 Valid
[  0.422] UART loader check trigger.
[  1.427] Check USB flash media.
[  2.430] No valid firmware found on flash media, status=1
[  2.436] Verify slot 1 header.
[  2.637] Slot 1 has firmware header.
[  2.838] Slot 1 is ready.
[  2.840] Check for update.
[  2.843] Verify slot 0.
[  2.845] Verify slot 0 header.
[  3.050] Verify slot 0 signature.
[  3.072] Verify slot 0 ready.
[  3.075] Verify slot 0 fw ver.
[  3.279] Slot 0 has valid active firmware version 1.3.0
[  3.284] Slot 1 firmware 1.3.1 is newer.
[  3.288] Prepare for update.
[  3.291] Verify slot 1 signature.
[  3.357] Erase slot 0.
[................                ] 50%
[ 14.138] Copy slot 1 to slot 0.
[................                ] 51%
[.................               ] 52%
[.................               ] 53%
[.................               ] 54%
[..................              ] 55%
[..................              ] 56%
[..................              ] 57%
[...................             ] 58%
[...................             ] 59%
[...................             ] 60%
[....................            ] 61%
[....................            ] 62%
[....................            ] 63%
[....................            ] 64%
[.....................           ] 65%
[.....................           ] 66%
[.....................           ] 67%
[......................          ] 68%
[......................          ] 69%
[......................          ] 70%
[.......................         ] 71%
[.......................         ] 72%
[.......................         ] 73%
[........................        ] 74%
[........................        ] 75%
[........................        ] 76%
[.........................       ] 77%
[.........................       ] 78%
[.........................       ] 79%
[..........................      ] 80%
[..........................      ] 81%
[..........................      ] 82%
[...........................     ] 83%
[...........................     ] 84%
[...........................     ] 85%
[............................    ] 86%
[............................    ] 87%
[............................    ] 88%
[............................    ] 89%
[.............................   ] 90%
[.............................   ] 91%
[.............................   ] 92%
[..............................  ] 93%
[..............................  ] 94%
[..............................  ] 95%
[............................... ] 96%
[............................... ] 97%
[............................... ] 98%
[................................] 99%
[................................] 100%
[ 14.937] Slot 0 validated.
[ 14.940] Verify slot 0.
[ 14.942] Verify slot 0 header.
[ 15.143] Verify slot 0 signature.
[ 15.165] Slot 0 has valid firmware.
[ 15.168] Preparing to launch application in slot 0.

TestApp starting...


======================================================================
=                                                                    =
=        stm32-secure-patching-bootloader Test Application           =
=                                                                    =
======================================================================
  Board: DISCO-L4R9I (32L4R9IDISCOVERY)
  FW Version: 1.3.1
  FW Build: v1.3.0-preview1-dirty
  FW Tag: 0x9556B635
  OSPI External Flash string: This is a version 2 message from OSPI External Flash!
  Version 2

```
