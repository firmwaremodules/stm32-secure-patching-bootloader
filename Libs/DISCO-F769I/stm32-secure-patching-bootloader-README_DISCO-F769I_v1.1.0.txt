# Board configuration 

/* Configuration for 2  MB flash device.
 * 
 * internal sector size: 256K
 * external sector size: 64K
 *   
 *  STM32F7 Internal flash                           MX25L512G External flash
 * -----------------------------------------------   -------------------------------------------------
 * | SBSFU  | U |  SLOT0 SEG0 7 sectors          |   | SLOT0 SEG1 X sectors | SLOT1 7 + X sectors | ...
 * -----------------------------------------------   -------------------------------------------------
 *   128     128          1792                           256*X                     1792 + 256*X
 * 
 * Offsets given X = 16 (4 MB SEG1)
 *
 * 0x08000000
 *          0x08020000
 *              0x08040000
 *                                 
 *                                               0x081FFFFF
 *                                                   0x90000000             
 *                                                                          0x90400000
 *                                                                                                0x909BFFFF
 *                                     
 *
 * X - number of 256K sectors to assign to storing application resources in QSPI area.
 * U - unused/available sector 128K.
 *
 */

YMODEM loader: YES
UART1 115200,8,N,1

USB flash loader: YES



