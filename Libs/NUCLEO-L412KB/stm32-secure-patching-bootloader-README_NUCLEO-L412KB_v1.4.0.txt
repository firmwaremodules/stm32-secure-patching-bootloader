# Board configuration 

/* Configuration for 128 KB flash device, NO QSPI
 * 
 * Internal sector size: 2K
 *
 * Single slot mode (no patch file .sfbp support)
 * 
 * -------------------------------------------
 * | SBSFU  |  SLOT0                         |  
 * -------------------------------------------
 *    64            64                        
 * 
 * 0x08000000
 *          0x08010000
 *                                           0x08020000
 *
 */

YMODEM loader: YES
UART2 115200,8,N,1

USB flash loader: NO
