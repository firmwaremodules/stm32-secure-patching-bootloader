## STM32 Secure Patching Bootloader
A Secure Patching Bootloader and Firmware Update System for **STM32** MCUs.

The only bootloader and firmware update system you may ever need.  Works with almost any STM32 MCU family using the [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html) development environment.

This unique solution is an easy way to get a secure and robust bootloader that offers multiple firmware update methods built-in, including delta patching.  It is a plug'n'play system that requires no configuration and just works!

**Features:**

* Robust: dual slot (SLOT0 - active and SLOT1 - download) firmware updating.
* Secure: signed (ECDSA) and encrypted (AES) firmware update images (.sfb) and delta patches (.sfbp)
* Optional support for download slot (SLOT1) in external flash.
* Optional support for distributing active slot (SLOT0) firmware image over internal *and* external flash - known as *MultiSegment* capability - benefiting large applications like TouchGFx GUI systems that include assets that must be located in external flash.
* Firmware delta patching engine built-in and is accessible by both the bootloader and the application at runtime for powerful OTA delta updates.
* Multiple secure firmware update methods from bootloader: YMODEM over UART, USB flash drive (where available).
* Optional automatic 'git' semantic versioning support: automatically version your application firmware end-to-end with git repository tags.
* Progress messages printed to UART.

This secure patching bootloader and firmware update system is MIT licensed and free to use on any NUCLEO, DISCO or EVAL board we support here. If your NUCLEO, DISCO or EVAL board is missing, post an issue and we'll add it.

### Quick Start Guide

Refer to details in [Product Documentation](Docs/README.md).


### Supported Boards

This list will grow over time as we work to support key STM32 NUCLEO, DISCO, EVAL and 3rd-party boards.  Note that we group -DISCO, -Discovery and -DK  as just `DISCO`.

| Family | Boards |  |
| --- | --- | --- |
| STM32L0 | NUCLEO-L073RZ B-L072Z-LRWAN1 |
| STM32L4 | DISCO-L496G | 
| STM32WL | LORA-E5-DEV | *NEW* works on LORA-E5-MINI too |
| STM32F4 | NUCLEO-F429ZI |
| STM32F7 | DISCO-F769I |

Please post an issue if you'd like a particular board supported.

### Delta Patch Engine

The Delta Patch Engine is built into the bootloader and ready to be accessed by your application at runtime or by the bootloader through UART or USB flash drive updates.  The Delta Patch Engine features:

* Same security as regular full-image .sfb files.  The .sfbp patch container is secured with the same signed header and encrypted.
* Regenerates the full firmware update image into SLOT1 from the content of the patch and the content of the existing application in SLOT0.  The final result is as-if a full image .sfb update was performed (in fact exactly the same as the SHA256 digest will attest).
* Performs SHA256 digest check on the source image (SLOT0) and compares to expected digest embedded in the patch container before taking any action.
* Single-byte streaming update capability.  The patch engine can be fed any number of bytes at a time (including just 1 byte) to support any OTA update method.
* The installation of firmware (copy from SLOT1 to SLOT0) is always handled by the bootloader at startup and only occurs after the regenerated firmware image in SLOT1 has been verified and authenticated and the user application has requested or initiated a reboot.
* The patching engine API consists of just three functions (Init(), Data(), Finish()) described in one header file and implemented in one object file bound at link time.


### MultiSegment

The MultiSegment feature solves the problem of how to update monolithic applications that are larger than the device's internal flash, or equivalently, applications that that are linked to be executed in two disjoint flash regions - for example internal and external flash.

This problem is common with GUI systems where you might find a 300 KB firmware application coupled with 4 MB of GUI assets like images and videos and fonts etc. In advanced GUI systems like TouchGFx, these assets are accessed through regular MCU memory read instructions and must therefore be available in a program-readable memory region.
Since internal flash (at 0x0800 0000) is not large enough to hold all of these assets, a memory region dedicated to an external flash through the Q/OSPI peripheral on STM32 devices is used.  This region is typically assigned to 0x9000 0000.  

The application's linker script contains a section definition located at 0x9000 0000 to which all GUI assets are placed at link time.  The resultant .hex file remains compact because it contains just the data along with addresses to be written. 
Loading this .hex file with an external-flash-aware programmer like STM32CubeProgrammer works fine, but you do not have a bootloader nor capability to update your application and GUI assets in the field.

The stm32-secure-patching-bootloader with the MultiSegment feature abstracts away this low-level complexity from the bootloader and firmware update engines.  From their point of view, SLOT0 is a contiguous memory region of arbitrary size - it can be much larger than internal flash (i.e. 16 MB) - and will hold the entire application image including GUI assets.  

So what does MultiSegment mean to you?  It means you can build and deploy your 4 or 8 or 16 or 24 MB GUI application as easily and seamlessly as if it was a regular small 300 KB application that fits entirely and neatly in your MCUs internal flash.  Furthermore, the delta patching feature built into the stm32-secure-patching-bootloader
offers a huge benefit for large applications. Imagine changing only functionality or fixing a bug in your 16 MB combined application.  With delta patching, only the difference - the .sfbp patch file - needs to be distributed to your customers and/or devices in the field, potentially a few hundred to few thousand bytes.  If you had to distribute this over a wireless link think of the savings in bandwidth and cost and time you would realize!
The stm32-secure-patching-bootloader's USB flash drive update feature is also a great way to update devices in the field with patches or full images - after all, GUI devices are built for human interaction and often don't necessarily have wireless links but may have an exposed USB port.

See this [MultiSegment Graphic](Docs/stm32-secure-patching-bootloader-MultiSegment_rev1_Dec2021.pdf) illustrating slot placement.


### Release Notes

**v1.1.0  - May 2022**

* Adds new platform support for STM32WLE5 and SeeedStudio LORA-E5-DEV and LORA-E5-MINI boards.   
* Adds specific support for the B-L072Z-LRWAN1 board. 
* Adds README to each library package to describe flash layout and bootloader configuration. 
* Changes postbuild command to allow user to specify location of bootloader Libs directory. 
* Removes vector offset and multiseg address parameters in the postbuild command script (these are now defined in the bootloader library package artifacts). 

**v1.0.0 - Dec 2021**

* Initial Release 



























