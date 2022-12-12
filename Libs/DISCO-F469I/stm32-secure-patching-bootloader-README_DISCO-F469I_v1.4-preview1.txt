# Board configuration 

/* Note: all flash configurations assume *dual bank* mode.
 The F469 2 MB device only operates in dual bank mode. 
 The 1 MB device can operate in either single or dual bank.
 With dual bank mode, the internal flash sectors are not uniform however
 this is not a problem for the bootloader.
 */

/* Configuration for 2  MB flash device.
 * 
 * internal sector size: 16,64,128K
 * external sector size: 64K
 *
 * To work with the limited external flash and the STM32469I-Discovery TouchGFX demo,
 * we allocate half, 8 MB, to SLOT1.  Thus SLOT0 is also 8 MB and split up as 1 MB SEG0 and 7 MB SEG1.
 * The touchGFX app's QSPI section has to fit into 7 MB.  The Demo app cuts out the "Bird Eat Coin"
 * Game2D images when TOUCHGFX_DISABLE_GAME2D is defined in STM32CubeIDE for C++ preprocessor.

 * Allocating 8 MB to SLOT0 and SLOT1.  SLOT0 SEG1 holds the GUI assets assigned to "ExtFlashSection" area.
 *   
 *  STM32F469 Internal flash                          N25Q128A  16 MB external flash
 * -------------------------------------------   ------------------------------------------------
 * | SBSFU  |  SLOT0 SEG 0       | Unused    |   | SLOT0 SEG 1      | U |   SLOT1               |
 * -------------------------------------------   ------------------------------------------------
 *   128           1024                                7168                   8192
 * 
 *
 * 0x08000000
 *          0x08020000
 *                               0x0811FFFF  
 *                                           0x081FFFFF
 *                               
 *                                               0x90000000                
 *                                                                  0x906FFFFF 
 *                                                                         0x90400000
 *                                                                                               0x90FFFFFF
 */


| Feature   | DISCO-F469I | 
| ---       | ---         |
| NAME      | 32F469IDISCOVERY
| STATUS    | Active
| UART      | USART3 TX:PB10 RX:PB11 AF7  115200,8,N,1
| BUTTON    | PA0 ACTIVE HIGH 
| LED       | GREEN/LED1/PG6
| FLASH     | 2048
| RAM       | 320 (160 SRAM1 + 32 SRAM2 + 128 SRAM3)
| DEVID     | 0x434
| CLK       | HSE,8,180
| YMODEM    | YES
| USB       | YES  PWR: PB2
| EXT FLASH | YES  128 Mb QUADSPI N25Q128A
| MULTISEG  | YES  0x90000000 (QUADSPI1)
| Product   | https://www.st.com/en/evaluation-tools/32f469idiscovery.html



