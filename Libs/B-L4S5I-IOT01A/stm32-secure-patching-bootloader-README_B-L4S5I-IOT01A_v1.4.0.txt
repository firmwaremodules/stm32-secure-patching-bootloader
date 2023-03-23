# Board configuration 

/* Configuration for 2  MB flash device.
 * internal sector size: 4K (dual bank mode - default)
 *   
 *  STM32L4S5 Internal flash        
 * -------------------------------------------- -------------------
 * | SBSFU  |  SLOT 0              | SLOT1                        |
 * ----------------------------------------------------------------
 *   80              984                         984
 * 
 * 0x08000000
 *          0x08014000
 *                                 0x08109FFF
 *                                  0x0810A000
 *
 *                                                                 0x081FFFFF
 */

| Feature   | B-L4S5I-IOT01A | 
| ---       | ---         |
| NAME      | B-L4S5I-IOT01A
| UART      | USART1 TX:PB6 RX:PB7 AF7  115200,8,N,1
| BUTTON    | PC13 ACTIVE LOW 
| LED       | GREEN/LED2/PB14
| FLASH     | 2048
| RAM       | 640 (192 SRAM1 + 64 SRAM2 + 384 SRAM3)
| DEVID     | 0x470
| CLK       | MSI,40,120,HSI48 
| YMODEM    | YES
| USB       | NO "User must add 8 MHz crystal at X1 to use USB OTG"
| EXT FLASH | NO
| MULTISEG  | NO
| Product   | https://www.st.com/en/evaluation-tools/b-l4s5i-iot01a.html

