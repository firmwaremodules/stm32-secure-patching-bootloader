# Board configuration 

 *  STM32L5 Internal flash 512 KB                   
 * -------------------------------------------------
 * | SBSFU  | U | SLOT0          |  SLOT1          |  
 * -------------------------------------------------
 *   64      64     192                192
 * 
 * 0x08000000
 *          0x08010000
 *              0x08020000
 *                              0x0804FFFF
 *                               0x08050000
 *                                                 0x0807FFFF
 *
 * U - unused/available sector(s)


| Feature   | DISCO-L562E | 
| ---       | ---         |
| NAME      | STM32L562E-DK
| UART      | USART1 TX:PA9 RX:PA10 AF7  115200,8,N,1
| BUTTON    | PC13 ACTIVE HIGH
| LED       | GREEN/LED10/PG12
| FLASH     | 512
| RAM       | 256 (192 SRAM1 + 64 SRAM2)
| DEVID     | 0x472
| CLK       | MSI,4,110
| YMODEM    | YES
| USB       | NO "The STM32L562E-DK Discovery kit supports USB Type-C sink mode only."
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/stm32l562e-dk.html

