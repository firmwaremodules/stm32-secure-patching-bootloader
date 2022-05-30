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

YMODEM loader: YES
UART1 115200,8,N,1



