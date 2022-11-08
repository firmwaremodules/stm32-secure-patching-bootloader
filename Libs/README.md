## STM32 Secure Patching Bootloader

## Libraries

In the `Libs` directory you will find the two key files needed by your application and build system to implement a secure bootloader and patching firmware update system:

1. `stm32-secure-patching-bootloader_<BOARD>_<version>.bin` : pre-built binary ready to run on the specified board.
2. `stm32-secure-patching-bootloader-linker-gcc_<BOARD>_<version>.ld` : application linker script configuration definitions.

The capabilities built into the stm32-secure-patching-bootloader are dependent on the board it is targeting.  For example, on boards that support USB host, the ability to update from USB flash drives may have been integrated and enabled.  
On boards that offer external flash, the multi-segment feature may have been enabled to allow placement of a portion of SLOT0 and all of SLOT1 in external flash.



