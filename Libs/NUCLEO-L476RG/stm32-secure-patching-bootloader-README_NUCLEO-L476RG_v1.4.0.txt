# Board configuration 

/* Configuration for 1  MB flash device STM32L476RG
 * 
 * Internal sector size: 2K
 * 
 * ------------------------------------------------------------------------
 * | SBSFU  |  SLOT0                         |   SLOT1              | ... |
 * ------------------------------------------------------------------------
 *    80            256                           256             
 * 
 * 0x08000000
 *          0x08014000
 *                                           0x08054000
 *                                                                  0x08094000             
 */

Note: built for MB1136 C-02 or C-03 with LSE.

| Feature   | NUCLEO-L476RG | 
| ---       | ---         |
| NAME      | NUCLEO-L476RG
| UART      | USART2 TX:PA2 RX:PA3 115200,8,N,1
| BUTTON    | PC13 ACTIVE LOW 
| LED       | GREEN/LED2/PA5 ACTIVE HIGH
| FLASH     | 1024
| RAM       | 96
| DEVID     | 0x415
| CLK       | MSI,4,80
| YMODEM    | YES, button trigger, 'load' trigger
| USB       | NO
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/nucleo-l476rg.html



