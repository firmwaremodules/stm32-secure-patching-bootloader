# Board configuration 

/* Configuration for 192  KB flash device
 *
 * Internal write protection sector size: 4K, erase page is 128 bytes.
 * Setup slot sizing for the debug mode on 4K boundaries.
 *
 * ------------------------------------------------------------------
 * | SBSFU  |  SLOT0                         |   SLOT1              |
 * ------------------------------------------------------------------
 *   56 (14)          68 (17)                         68 (17)         
 * 
 * 0x08000000
 *          0x0800E000
 *                                           0x0801F000
 *                                                                  0x0802FFFF
 *
 */

YMODEM loader: YES
UART1 115200,8,N,1



