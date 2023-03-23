# Board configuration 

/* Configuration for 2  MB flash device.
 * *SINGLE BANK MODE*
 *
 * internal sector size: 128K
 *
 * Only allocate 256K for each slot.
 *   
 *  STM32F429 Internal flash                          
 * ------------------------------------------------------------------------------------------------
 * | SBSFU  |  SLOT0 2 sectors  | SLOT1 2 sectors | ...
 * ------------------------------------------------------------------------------------------------
 *   128      256                   256
 * 
 *
 * 0x08000000
 *          0x08020000
 *                                 
 *                              0x085FFFFF
 *                               0x08060000             
 *                                                 0x0809FFFF

| Feature   | NUCLEO-F429ZI | 
| ---       | ---         |
| NAME      | NUCLEO-F429ZI
| STATUS    | Active
| UART      | USART3 TX:PD8 RX:PD9 AF7  115200,8,N,1
| BUTTON    | PC13 ACTIVE HIGH 
| LED       | GREEN/LED1/PC7
| FLASH     | 2048
| RAM       | 192
| DEVID     | 0x419
| CLK       | HSE,8,168
| YMODEM    | YES
| USB       | YES  PWR: PG6 ACTIVE LOW
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/nucleo-f429zi.html



