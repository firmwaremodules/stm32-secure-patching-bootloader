## STM32 Secure Patching Bootloader

## Documentation Overview

* [Graphic](stm32-secure-patching-bootloader-MultiSegment_rev1_Dec2021.pdf) describing MultiSegment feature in more detail.
* [Quick Start Guide](stm32-secure-patching-bootloader-QSG_rev3_Nov2022.pdf) in PDF form with screenshots.

## Quick Start Guide

Integrating the stm32-secure-patching-bootloader is a simple five step process: 
1. Adding bootloader files to your project repository.
2. Configuring STM32CubeIDE.
3. Adjusting your project's linker script .ld file.
4. Adjusting your project's system_stm32xxxx.c file.
5. Generating your project's encryption and signing keys.

Please refer to [stm32-secure-patching-bootloader-demoapp](https://github.com/firmwaremodules/stm32-secure-patching-bootloader-demoapp) repository for working projects already implementing these steps or to the STM32 Cube repositories we maintain that has the bootloader integrated with select reference projects at [here](https://github.com/orgs/firmwaremodules/repositories).

Also refer to this [Quick Start Guide](stm32-secure-patching-bootloader-QSG_rev3_Nov2022.pdf) PDF document for more details including images and screenshots.

1. Adding bootloader files to your project repository

  * Create a directory called `Bootloader` in your project root.
  * Copy the directories `Include`, `Linker`, `Scripts`, `Tools` into it.
  * Copy the `Libs` directory, but only the board subdirectories that you are needing.  E.g. copy DISCO-F769I directory into your Libs directory if you are using that board.
  * As an alternative, you can add the bootloader files as a git submodule with `git submodule add https://github.com/firmwaremodules/stm32-secure-patching-bootloader Bootloader`.

2. Configure STM32CubeIDE.

We need to add the postbuild command line and update the include and linker paths.

  * Update Post-build steps C/C++ Build -> Settings -> Build Steps  
  
```
"../../../../../../../Bootloader/Scripts/STM32CubeIDE/postbuild.sh" "${BuildArtifactFileBaseName}" "../../Keys" "../../../../../Binary" "../../../../../../../Bootloader/Libs"  "0.0.0" "v1.0.0" "DISCO-L4R9I" "v1.3.0"
 |                                                                   |                              |           |                       |                                       |       |       |               |      
 \- Name of postbuild script, relative to build dir                  |                              |           |                       |                                       |       |       |               |      
                                                                     |                              |           |                       |                                       |       |       |               |      
                                                                     \- Name of applcation build artifact (Build Artifact -> Artifact Name)                                     |       |       |               |      
                                                                                                    |           |                       |                                       |       |       |               |      
                                                                                                    \- Directory where Keys are, relative to build dir, according to DemoApp reference design.  |               |
                                                                                                                |                       |                                       |       |       |               |      
                                                                                                                \- Directory where Outputs are placed and patch reference binaries are found, relative to build dir, according to DemoApp reference design. 
                                                                                                                                        |                                       |       |       |               |
                                                                                                                                        \- Directory where bootloader libraries are, relative to build dir.     |
                                                                                                                                                                                |       |       |               |      
                                                                                                                                                                                \- 'To' version (version to build)  (auto-mode in this example)   
                                                                                                                                                                                        |       |               |      
                                                                                                                                                                                        \- 'From' version (reference for patch generation) (from v1.0.0 in this example)
                                                                                                                                                                                                |               |      
                                                                                                                                                                                                \- bootloader library to link with (in Libs dir)
                                                                                                                                                                                                                |      
                                                                                                                                                                                                                \- Version of bootloader library to link with (in Libs dir)
                                                                                                                                                                                    
```

  * Add path to bootloader include: C/C++ Build -> Settings -> MCU GCC Compiler -> Include paths : `../../../../../../../Bootloader/Include`

  * Add paths to bootloader linker files: C/C++ Build -> Settings -> MCU GCC Linker -> Miscellaneous : `-Xlinker -L ../../../../../../../Bootloader/Libs/NUCLEO-L073RZ -L ../../../../../../../Bootloader/Linker`

3. Adjust your application's linker script.

At minimum we need to tell the linker where your application's new start offset is in flash.  This is defined by the bootloader's linker configuration file `stm32-secure-patching-bootloader-linker-gcc_<BOARD>_<version>.ld`. 
It defines some symbols that we may need, minimally it is `STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START`.  Then your application's interrupt vector table has to be offset from this by the minimum size of your vector table (to account for the image header), also defined as `VECTOR_SIZE` in the linker configuration file.

```
/* For this example end of RAM on STM32L073 is 0x20005000 = 20 KB*/

APPLI_region_intvec_start__  = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START + VECTOR_SIZE;
APPLI_region_ROM_start    = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START  + VECTOR_SIZE + VECTOR_SIZE;
APPLI_region_ROM_length   = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_END - APPLI_region_ROM_start + 1;
APPLI_region_RAM_start    = STM32_SECURE_PATCHING_BOOTLOADER_RAM_START;
APPLI_region_RAM_length    = 0x20005000 - APPLI_region_RAM_start;

MEMORY
{
  ISR_VECTOR (rx)   : ORIGIN = APPLI_region_intvec_start__, LENGTH = VECTOR_SIZE
  APPLI_region_ROM  : ORIGIN = APPLI_region_ROM_start, LENGTH = APPLI_region_ROM_length
  APPLI_region_RAM  : ORIGIN = APPLI_region_RAM_start, LENGTH = APPLI_region_RAM_length
}
```

To your SECTIONS, add the following:

```
  ...

  /* Extra ROM section (last one) to make sure the binary size is a multiple of the AES block size (16 bytes) */
  .align16 :
  {
    . = . + 1;         /* _edata=. is aligned on 8 bytes so could be aligned on 16 bytes: add 1 byte gap */
    . = ALIGN(16) - 1; /* increment the location counter until next 16 bytes aligned address (-1 byte)   */
    BYTE(0);           /* allocate 1 byte (value is 0) to be a multiple of 16 bytes                      */
  } > APPLI_region_ROM

  ...

```

A multi-target generic linker script that works with most STM32 targets is provided in the bootloader `Linker` directory.  See this [reference project linker script](https://github.com/firmwaremodules/stm32-secure-patching-bootloader-demoapp/tree/main/App/Project/DemoApp/NUCLEO-L073RZ/STM32CubeIDE/DemoApp_NUCLEO-L073RZ/STM32L073RZTx.ld).

For a TouchGFx multi-segment application (assets on external QSPI or OSPI flash), use this template:

```
/* For this example end of RAM on STM32L4R9I is 0x200A0000 = 640 KB*/ 
INCLUDE stm32-secure-patching-bootloader-linker-gcc_DISCO-L4R9I_v1.3.0.ld 

APPLI_region_intvec_start__  = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START + VECTOR_SIZE; 
APPLI_region_ROM_start    = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_START  + VECTOR_SIZE + VECTOR_SIZE; 
APPLI_region_ROM_length   = STM32_SECURE_PATCHING_BOOTLOADER_SLOT0_END - APPLI_region_ROM_start + 1; 
APPLI_region_RAM_start    = STM32_SECURE_PATCHING_BOOTLOADER_RAM_START; 
APPLI_region_RAM_length    = 0x200A0000 - APPLI_region_RAM_start; 

MEMORY 
{ 
  ISR_VECTOR (rx)   : ORIGIN = APPLI_region_intvec_start__, LENGTH = VECTOR_SIZE 
  APPLI_region_ROM  : ORIGIN = APPLI_region_ROM_start, LENGTH = APPLI_region_ROM_length 
  APPLI_region_RAM  : ORIGIN = APPLI_region_RAM_start, LENGTH = APPLI_region_RAM_length  
  QSPI (rx)         : ORIGIN = STM32_SECURE_PATCHING_BOOTLOADER_MULTISEG_START, LENGTH = 64M 
} 

```

To your SECTIONS, add the following:    

```
  /* Extra ROM section (last one) to make sure the binary size is a multiple of the AES block size (16 bytes) */ 
  .align16 : 
  { 
    . = . + 1;         /* _edata=. is aligned on 8 bytes so could be aligned on 16 bytes: add 1 byte gap */ 
    . = ALIGN(16) - 1; /* increment the location counter until next 16 bytes aligned address (-1 byte)   */ 
    BYTE(0);           /* allocate 1 byte (value is 0) to be a multiple of 16 bytes                      */ 
  } > APPLI_region_ROM 

  /* Section for placement of resources into QSPI segment  
   * This is not contiguous with the "ROM" segment, but must also be aligned 
   * to 16 bytes for AES requirement. 
   */ 
  ExtFlashSection :  
  {  
    *(ExtFlashSection)  
    . = . + 1;         /* _edata=. is aligned on 8 bytes so could be aligned on 16 bytes: add 1 byte gap */ 
    . = ALIGN(16) - 1; /* increment the location counter until next 16 bytes aligned address (-1 byte)   */ 
    BYTE(0);           /* allocate 1 byte (value is 0) to be a multiple of 16 bytes                      */ 
  } >QSPI 
```


4. Adjust your system_stm32xxxx.c file.

This file programs the VTOR register (Vector Table Offset Register) by your application in the early startup phase so that interrupts invoke your application's handlers at the linked offset instead of the bootloader's.

```
extern uint32_t APPLI_region_intvec_start__;
#define INTVECT_START ((uint32_t)& APPLI_region_intvec_start__)

void SystemInit(void)
{
    ...

    /* Configure the Vector Table location add offset address ------------------*/
    SCB->VTOR = INTVECT_START;
}

```

5. Generating your projects encryption and signing keys.

Use the make_keys.bat script under Scripts to call a Python tool to generate the AES encryption key (firmware confidentiality) and the ECDSA public verification and private signing keys (firmware authenticity).   Example on Windows systems to place keys in a Keys directory: 

```
c:\stm32-secure-patching-bootloader-demoapp\Bootloader\Scripts>make_keys.bat ..\..\App\Project\DemoApp\DISCO-F769I\STM32CubeIDE\Keys 

make_keys.bat : Generate new secure keys for stm32-secure-patching-bootloader 
Making ..\..\App\Project\DemoApp\DISCO-F769I\STM32CubeIDE\Keys/Cipher_Key_AES_CBC.bin 
Making ..\..\App\Project\DemoApp\DISCO-F769I\STM32CubeIDE\Keys/Signing_PrivKey_ECC.txt 
```

Run `make_keys <path to directory to contain key files>`

If youre not using Windows, then all you need to do is look inside make_keys.bat and run the Python scripts directly.  The Keys directory is referenced by the postbuild.sh post-build command line in the IDE.  This directory can be anywhere and called anything by adjusting the post-build command line. 

**Important Note**

These keys are also used by the bootloader to differentiate between compatible firmware loads!  That is, the stm32-secure-patching-bootloader will attempt to update to any firmware that is presented that can be successfully decrypted and signature verified. There is no product ID field in the header.  The keys are the product ID.  Of course, the point of having this type of security is to prevent loading of firmware except for those loads you explicitly authorize by way of signing during the build (automatically done by postbuild.bat).  But if you are running multiple products or even incompatible hardware revisions within the same product line, you must ensure to have unique keys setup for each STM32CubeIDE build project (the path to the keys is specified in the postbuild.sh post-build command line and in these examples is called Keys). 


**That's it.**  There is a bit to do here, but all things considered it is pretty minimal and your application sources and build procedure is virtually untouched by the addition of the stm32-secure-patching-bootloader.


### Build Products

The stm32-secure-patching-bootloader postbuild process produces three or four artifacts and places them in the specified output directory (`Binary` in the above).

Naming convention: 

*Combined binary:*

* ` BOOT_<Your Artifact Name>_<Board Name>_<version>.[hex | bin]`

*Update binary:*

* `<Your Artifact Name>_<Board Name>_<version>.[sfb | sfbp]`

Combined binaries are for loading onto the target by a programming tool such as STM32CubeProgrammer during production. 

Update binaries are for distribution to customers or to your apps and cloud services for in-field updates. 

  1. Combined binaries: `BOOT_DemoApp_NUCLEO-L073RZ_v1.0.0.hex`, `BOOT_DemoApp_NUCLEO-L073RZ_v1.0.0.bin` (.bin produced only when multisegment is not enabled)
  2. Secured in-field firmware full update file: `DemoApp_NUCLEO-L073RZ_v1.0.0.sfb` (full image) 
  3. Secured in-field firmware patch update file: `DemoApp_NUCLEO-L073RZ_v1.0.0_v1.1.0.sfbp` (patch - produced only if reference version v1.0.0 exists in `Binary\PatchRef`)

Note: the `<version>` appended to the file names is a direct copy of either the post-build command-line's to version, or else of the output of git decribe tags always dirty if the to version is in auto mode 0.0.0 or 0.  When using the auto mode (recommended), use git tagging to set the version.  A semantic version tag may be prepended with a v or not.  Firmware Modules projects like to prepend versions with a v, so a tag might be v1.3.1.  Either way works. 

Also note: the firmware image header contains a 4-byte field for version and therefore cannot directly accommodate a non-semantic version such as v1.3.1-7-gc32667a that may arise during development load testing.  The version generator embedded into the postbuild.sh script can safely handle this scenario by adding the number of commits since value to the build number, so v1.3.1-7 becomes 1.3.8 in the header. 

### Notes

#### General Notes

* Patch files .sfbp only work if the source version already exists on the target device.  E.g. to update from v1.1.7 to v1.2.0, version v1.1.7 must exist on the device as the active image in SLOT0.

* To update from v1.0.0 to v1.4.0 when only patches of v1.0.0_v1.1.0, v1.1.0_v1.2.0, v1.2.0_v1.3.0, v1.3.0_v1.4.0 are available, each patch must be applied in series.  For each one, firmware is installed by the bootloader through a reboot cycle.

* The build system (STM32CubeIDE) postbuild command line must explicitly set what the reference firmware version is to build a patch from.  With this flexibility it is possible to build patches from any version.  Commonly this 'from version' is updated from one release to the next to build a series of patchable updates (v1.0.0->v1.1.0, v1.1.0->v1.2.0 etc).  Of course you could create a patch from v1.0.0->v1.2.0 and post this to your update server; if your 'patch picker' algorithm was smart enough it could select the best patch from a list of available patches.

* Full image files .sfb can be used to update to any version and do not depend on what is currently on the device.  These could serve as a fall-back in case the hypothetical 'patch picker' implemented in the user application cannot find a suitable patch for download.

* The 'patch picker' is implemented in the USB flash drive updater to select the first patch in the root directory that matches the current version on the device and contains the highest 'to' version.  It is able to perform a 'patch chain' update as described above by repeatedly rebooting and updating to the next higher patch version.

#### Security Notes

* The stm32-secure-patching-bootloader strikes a balance between ease of integration, broad platform support and selection of security features that are enabled. 

* The bootloader system is designed so that your products and firmware update files can be distributed into uncontrolled environments.  This means firmware confidentiality is ensured through AES encryption, and firmware and device integrity are ensured through ECDSA (digital signatures).  The AES encryption and the ECDSA public verification keys are stored in your devices internal flash.  The AES encryption and ECDSA private signing key are typically stored in your firmware development repository (e.g. on GitHub, your developers and build PCs).  

* Those that would attempt to undermine your products and solutions know that these keys exist.  Thus, protection of these keys is paramount.  You must create a root of trust on each of the devices you deploy by way of enabling RDP Level 2 through the stm32-secure-patching-bootloader production build (you get this build when you register the bootloader at firmwaremodules.com).  This build will automatically check and enable RDP Level 2 on each boot to help mitigate potential RDP regression attack vectors (yes these do exist).  Note that when RDP Level 2 is enabled, you permanently forfeit the ability to connect a debugger to your devices (a good thing when security is concerned). 

* The bootloader system is not designed to protect your device and secrets from your own firmware application.  If you dont trust your application or the way it works (e.g. you think it might offer a way for an attacker to read out contents of memory) then this bootloader system is not for you, or at least you must be aware that internal protections such as proprietary readout protection (PCROP) or firewalls are not implemented.  These are by no means foolproof even when enabled.  Dont offer a command-line interface that has memory peek and poke commands. 

* Finally, you should assume that if an attacker has physical access to your device and is determined enough (time and resources) then your secrets will eventually be extracted.  You need to weigh the expense and effort someone (or some group) would go to obtain your firmware update AES encryption key and public signature verification key, and the payoff that may be associated with that effort.   
