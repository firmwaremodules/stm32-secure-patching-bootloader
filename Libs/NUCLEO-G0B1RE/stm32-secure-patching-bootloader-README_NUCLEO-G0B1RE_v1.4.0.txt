# Board configuration 

/* Configuration for 512  KB flash device
 *
 * Internal erase and write protection sector size: 2K
 * Setup slot sizing for the debug mode on 2K boundaries.
 *
 * ------------------------------------------------------------------
 * | SBSFU  |  SLOT0                         |   SLOT1              |
 * ------------------------------------------------------------------
 *   64              224                         224      
 * 
 * 0x08000000
 *          0x08010000
 *                                          0x08047FFF
 *                                           0x08048000
 *                                                                  0x0807FFFF
 *
 */


| Feature   | NUCLEO-G0B1RE | 
| ---       | ---         |
| NAME      | NUCLEO-G0B1RE
| UART      | USART2 TX:PA2 RX:PA3 115200,8,N,1
| BUTTON    | PC13 ACTIVE LOW 
| LED       | GREEN/LED2/PA5
| FLASH     | 512
| RAM       | 144 (no parity check)
| DEVID     | 0x467
| CLK       | HSI,64
| YMODEM    | YES, button trigger, 'load' trigger
| USB       | NO
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/nucleo-g0b1re.html



