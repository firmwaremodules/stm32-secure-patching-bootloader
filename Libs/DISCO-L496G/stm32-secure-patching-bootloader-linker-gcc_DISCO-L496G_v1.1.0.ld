/*
 * Copyright (c) 2021 Firmware Modules Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files(the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions :
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
 * OR OTHER DEALINGS IN THE SOFTWARE.
 */

/* !! DO NOT MODIFY !! 
 *
 * These are linker script constants that applications must use to successfully
 * interface with the stm32-secure-patching-bootloader of the same version.
*/

VECTOR_SIZE = 0x200;

STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START    = 0x08014000;
STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_END      = 0x08053FFF;

STM32_SECURE_PATCHING_BOOTLOADER_RAM_START      = 0x20001700;

SE_IF_REGION_ROM_START                          = 0x8007500;
SE_IF_REGION_ROM_LENGTH                         = 0xB00;
