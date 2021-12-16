## STM32 Secure Patching Bootloader

## Tools

These mostly Python tools serve two purposes:
1. Generate your application's firmware artifacts by postbuild script: combined bootloader+application .bin or .hex, firmware update files .sfb or .sfbp (patch).
2. Generate your application's secure keys: ECDSA and AES keys by make_keys script.

The [JojoDiff](http://jojodiff.sourceforge.net/) difference tool `jdiff.exe` v0.8.1 is obtained from https://sourceforge.net/projects/jojodiff/.


To use these scripts you need to make sure you have installed the appropriate Python modules listed in "requirements.txt":

* `pip install -r requirements.txt`

The scripts have been tested to work with Python 3.8.0 or later.


