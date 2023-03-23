# Board configuration 

/* Configuration for 512 KB flash device, NO QSPI
 * 
 * Internal sector size: 2K
 * 
 * ------------------------------------------------------------------------
 * | SBSFU  |  SLOT0                         |   SLOT1              | Rsvd |
 * ------------------------------------------------------------------------
 *    64            128                           128                 192
 * 
 * 0x08000000
 *          0x08010000
 *                                           0x08030000
 *                                                                  0x08050000             
 *                                                                          0x80080000
 *
 */

YMODEM loader: YES
UART2 115200,8,N,1

USB flash loader: NO

