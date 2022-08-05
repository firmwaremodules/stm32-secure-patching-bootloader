## STM32 Secure Patching Bootloader Board Test Instructions

1. Load `BOOT_TestApp_<BOARD>_vX.Y.0.bin` to the target with STM32CubeProgrammer.
2. Connect terminal program (e.g. TeraTerm) to board's VCOM port @ 115200,N,8,1. Power cycle or reset board.
3. Select update method: YMODEM from bootloader (hold user button while restarting, or paste code `load` during appropriate stage in boot process), or YMODEM from TestApp.
4. Test full image update: transfer `TestApp_<BOARD>_vX.Y.1.sfb` via terminal program YMODEM.
5. Or test patch update: transfer `TestApp_<BOARD>_vX.Y.0_vX.Y.1.sfbp` via terminal program YMODEM.
6. Or on boards that support USB OTG host, place files onto USB flash stick and have it inserted/connected to adapter connected to USB OTG port while restarting board.
