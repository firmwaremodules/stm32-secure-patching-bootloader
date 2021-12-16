## STM32 Secure Patching Bootloader

## Common Linker Script

Most applications and most targets can use the same linker script, provided that
certain target-specific preamble configuration is available.

This premable typically looks like this.  The target-specific vector table offset and
RAM size is incorporated into the constants.


```
/* Entry Point */
ENTRY(Reset_Handler)

/* Highest address of the user mode stack */
_estack = 0x20005000;    /* end of RAM specific to the device. */

/* Generate a link error if heap and stack don't fit into RAM
 * These do not reserve memory for these areas but rather just
 * ensure this amount is 'free' after everything else is placed.
 */
_Min_Heap_Size = 0x200;      /* required amount of heap  */
_Min_Stack_Size = 0x400;     /* required amount of stack */

INCLUDE stm32-secure-patching-bootloader-linker-gcc_<version>_<target>.ld

/* Specific ROM/RAM UserApp definition */
APPLI_region_intvec_start__  = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START + 0x200; /* Cortex-M7: 0x400, others: 0x200 */
APPLI_region_ROM_start    = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START  + VECTOR_SIZE + 0x200; /* Cortex-M7: 0x400, others: 0x200 */
APPLI_region_ROM_length   = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_END - APPLI_region_ROM_start + 1;
APPLI_region_RAM_start    = STM32_SECURE_PATCHING_BOOTLOADER_RAM_START;
APPLI_region_RAM_length    = 0x20005000 - APPLI_region_RAM_start;

/* Specify the memory areas */
MEMORY
{
 ISR_VECTOR (rx)   : ORIGIN = APPLI_region_intvec_start__, LENGTH = VECTOR_SIZE
 APPLI_region_ROM  : ORIGIN = APPLI_region_ROM_start, LENGTH = APPLI_region_ROM_length
 APPLI_region_RAM  : ORIGIN = APPLI_region_RAM_start, LENGTH = APPLI_region_RAM_length
 SE_IF_region_ROM (rx) : ORIGIN = SE_IF_REGION_ROM_START, LENGTH = SE_IF_REGION_ROM_LENGTH
 QSPI (rx)         : ORIGIN = APPLI_region_MULTISEG_start__, LENGTH = 64M
}

/* Include the SECTIONS (not target-specific) */
INCLUDE stm32-secure-patching-bootloader-app-linker-sections_<version>.ld

```

For *Multisegment and/or external (O)(Q)SPI flash targets* add a QSPI memory region and use the multiseg linker script:

```
MEMORY
{
 ISR_VECTOR (rx)   : ORIGIN = APPLI_region_intvec_start__, LENGTH = VECTOR_SIZE
 APPLI_region_ROM  : ORIGIN = APPLI_region_ROM_start, LENGTH = APPLI_region_ROM_length
 APPLI_region_RAM  : ORIGIN = APPLI_region_RAM_start, LENGTH = APPLI_region_RAM_length
 SE_IF_region_ROM (rx) : ORIGIN = SE_IF_REGION_ROM_START, LENGTH = SE_IF_REGION_ROM_LENGTH
 QSPI (rx)         : ORIGIN = APPLI_region_MULTISEG_start__, LENGTH = 64M
}

/* Include the SECTIONS (not target-specific) for multi-segment flash slot allocation */
INCLUDE stm32-secure-patching-bootloader-app-linker-sections-multiseg_<version>.ld

```
