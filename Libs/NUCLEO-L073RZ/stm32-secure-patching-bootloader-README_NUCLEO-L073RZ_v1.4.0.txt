# Board configuration 

/* Configuration for 192  KB flash device
 *
 * Internal write protection sector size: 4K, erase page is 128 bytes.
 * Setup slot sizing for the debug mode on 4K boundaries.
 *
 * ------------------------------------------------------------------
 * | SBSFU  |  SLOT0                         |   SLOT1              |
 * ------------------------------------------------------------------
 *   56 (14)          68 (17)                         68 (17)         
 * 
 * 0x08000000
 *          0x0800E000
 *                                           0x0801F000
 *                                                                  0x0802FFFF
 *
 */


| Feature   | NUCLEO-L073RZ | 
| ---       | ---         |
| NAME      | NUCLEO-L073RZ
| UART      | USART2 TX:PA2 RX:PA3 AF4  115200,8,N,1
| BUTTON    | PC13 ACTIVE LOW 
| LED       | GREEN/LED2/PA5
| FLASH     | 192
| RAM       | 20 
| DEVID     | 0x447
| CLK       | HSI,32
| YMODEM    | YES
| USB       | NO
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/nucleo-l073rz.html



