# Board configuration 

/* Configuration for 2  MB flash device.
 * Flash: 512 Mb OCTOSPI MX25LM51245GXDI00
 * internal sector size: 4K (dual bank mode - default)
 * external sector size: 4K, 32K or 64K (64K used as block)
 * SBSFU is around 82K fully loaded with External flash/Multiseg + USB flash loader
 *   
 *  STM32L4R9 Internal flash                           MX25LM51245G 64 MB External flash
 * ---------------------------------   -----------   -------------------------------------------------
 * | SBSFU  |  SLOT 0 SEG0         |   | SLOT0 SEG1 X sectors | SLOT1                       | ...    |
 * ---------------------------------   ---------------------------------------------------------------
 *   84              1964                         4096              1964 + 4096
 * 
 *
 * 0x08000000
 *          0x08015000
 *                                 
 *                                 0x081FFFFF
 *                                     0x90000000             
 *                                                            0x90400000
 *                                                                                         0x909EAFFF
 *                                                                                          0x909EB000
 *
 */

| Feature   | DISCO-L4R9I | 
| ---       | ---         |
| NAME      | 32L4R9IDISCOVERY
| STATUS    | Active (8-11-22)
| UART      | USART2 TX:PA2 RX:PA3 AF7  115200,8,N,1
| BUTTON    | (JOY-SEL) PC13 ACTIVE HIGH 
| LED       | GREEN/LED2/PH4
| FLASH     | 2048
| RAM       | 640 (192 SRAM1 + 64 SRAM2 + 384 SRAM3)
| DEVID     | 0x470
| CLK       | MSI,40,120,HSI48 
| YMODEM    | YES
| USB       | YES  PWR: MFX_GPIO13
| EXT FLASH | YES  512 Mb OCTOSPI MX25LM51245GXDI00
| MULTISEG  | YES  0x90000000 (OCTOSPI1)
| Product   | https://www.st.com/en/evaluation-tools/32l4r9idiscovery.html
