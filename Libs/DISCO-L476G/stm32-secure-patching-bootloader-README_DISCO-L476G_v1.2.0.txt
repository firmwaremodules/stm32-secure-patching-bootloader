# Board configuration 

/* Configuration for 1  MB flash device, NO QSPI
 * 
 * internal sector size: 2K
 * SBSFU is around 71K fully loaded with ALL debug output
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
 *                                                                          0x90400000
 */

YMODEM loader: YES
UART2 115200,8,N,1

USB flash loader: YES

Note: built for REVB or REVC MB1184.

