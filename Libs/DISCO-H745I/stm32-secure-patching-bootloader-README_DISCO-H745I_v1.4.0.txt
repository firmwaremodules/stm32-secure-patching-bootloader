# Board configuration 

/* Configuration for 2  MB flash device.
 * 
 * internal sector size: 128K
 * external sector size: 64Kx2 = 128K
 *   
 *  STM32H745I Internal flash                              mt25tl01g External flash dual-die 256x2 Mb
 * -------------------------------------------   -----------------------------------------------------------
 * | BOOT   | SLOT0 SEG0                     |   | SLOT0 SEG1           | SLOT1                  |  Unused |
 * -------------------------------------------   -----------------------------------------------------------
 *   128              1920                           2176                  4096
 * 
 *
 * 0x08000000
 *          0x08020000
 *                                           0x081FFFFF
 *                                               0x90000000             
 *                                                                      0x90220000
 *                                                                                               0x90620000
 *                                     
 *
 *
 */

| Feature   | DISCO-H745I | 
| ---       | ---         |
| NAME      | STM32H745I-DISCO
| STATUS    | Active
| UART      | USART3 TX:PB10 RX:PB11 AF7  115200,8,N,1
| BUTTON    | B1 PC13 ACTIVE HIGH 
| LED       | GREEN/LD7/USER2/PJ2
| FLASH     | 2048 KB (dual bank, contiguous) @ 0x08000000.
|           | Cortex-M7 default boot from @ 0x08000000 (bank1)
|           | Cortex-M4 default boot from @ 0x08100000 (bank2)
| RAM       | DTCM  128 KB  @ 0x20000000
|           | AXI   512 KB  @ 0x24000000  *BOOT runs and is resident here*
|           | SRAM1 128 KB  @ 0x30000000
|           | SRAM2 128 KB  @ 0x30020000
|           | SRAM3 32  KB  @ 0x30040000
|           | SRAM4 64  KB  @ 0x38000000
| DEVID     | 0x450
| CLK       | HSE,25,400 
| YMODEM    | YES
| USB       | YES  PWR: PA5 ACTIVE HIGH
| EXT FLASH | YES  256+256 Mbit QUADSPI MT25TL01G dualmode configuration (stacked-die)
| MULTISEG  | YES  0x90000000 (QUADSPI)
| Product   | https://www.st.com/en/evaluation-tools/stm32h745i-disco.html



