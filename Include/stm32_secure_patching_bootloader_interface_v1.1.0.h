/**
******************************************************************************
* @file    stm32_secure_patching_bootloader_interface.h
* @brief   Application interface to stm32-secure-patching-bootloader.
******************************************************************************
*/
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

 /**
   * @brief  Secure Engine Error definition
   */
typedef enum
{
    SE_ERROR = 0U,
    SE_SUCCESS = !SE_ERROR
} SE_ErrorStatus;


/**
  *  @brief  Secure Engine Status definition
  */
typedef enum
{
    SE_OK = 0U,                                        /*!< Secure Engine OK */
    SE_KO,                                             /*!< Secure Engine KO */
    SE_INIT_ERR,                                       /*!< Secure Engine initialization error */
    SE_BOOT_INFO_ERR,                                  /*!< An error occurred when accessing BootInfo area */
    SE_BOOT_INFO_ERR_FACTORY_RESET,                    /*!< A factory reset has been executed to recover the BootInfo Initialization failure */
    SE_SIGNATURE_ERR,                                  /*!< An error occurred when checking FW signature (Tag) */
    SE_ERR_FLASH_READ                                  /*!< An error occurred trying to read the Flash */
} SE_StatusTypeDef;

/*!
* Provides services for applications to update firmware in accordance with
* the Firmware Modules' Application Management and Deployment Model.
*
* The application (APP) and manufacturing test application (MTA) sections in
* the target non-volatile storage may be updated by presenting an update firmware
* image that was generated with FM_Release.  The Update module takes care of
* choosing the correct APP section (APP1 or APP2) so as to support over-the-air
* streaming firmware updating that is highly tolerant to link or device failure -
* the target device's running application remains safe at all times during this
* process.
*
* Update APIs will NOT update firmware to older versions.  If an older version (i.e. a 'downgrade')
* is required, the changes must be reverted/implemented then built with a new version number.
* The Update and AMDM system uses only the version number to determine which application
* to boot and which application to overwrite when updating.
*
* The Update module does not maintain its own RAM buffer but rather utilizes
* the buffers provided by existing packet transport infrastructure.  The only
* requirement on these buffers is that the *first* buffer provided must contain
* at least {@link #getMinUpdateImageDataLen} bytes.  This value is platform
* dependent, therefore transport buffer sizing must take this value into account as well.
* The first buffer must contain enough bytes to verify that a firmware image is
* indeed being supplied to the update engine.  The actual firmware image length is
* extracted from the content of the first buffer supplied to {@link #data}.
*
* @a(Security Policies)
* It is strongly advised to use a secure transport for data (for both commands and firmware images)
* provided over the air to the APIs in this module.
*
* @a(Thread Safety)
* The APIs in this module are NOT thread-safe
* and must all be called from the same context, or unpredictable results
* may occur.
*
* @a(Other Notes)
* The reboot delay "window" is not supported at this time.  Specifying a delay
* other than RebootDelay_IMMEDIATE or RebootDelay_COMMAND to {@link #start} will
* be rejected.
*
*/

#include <stdbool.h>
#include <stdint.h>

/*!
* @value(StatusCode_NONE) No status code
* @value(StatusCode_COMPLETED) Response to a completed API call or the update has completed in case of status poll
* @value(StatusCode_INVALID_ARG) Response to an invalid API argument
* @value(StatusCode_INVALID_IMAGE) Reponse to early header verification failure
* @value(StatusCode_IMAGE_TOO_LARGE) Fail if provided length is too large, or embedded image length is too large
* @value(StatusCode_IMAGE_TOO_SMALL) Fail if embedded image length is smaller than the minimum data length
* @value(StatusCode_SECTION_NOT_AVAILABLE) Non-volatile section corresponding to the supplied ImageType cannot be found
* @value(StatusCode_SECTION_ERASE_FAILURE) Error preparing (erasing) update target section
* @value(StatusCode_SECTION_WRITE_FAILURE) Error writing data to update target section
* @value(StatusCode_IMAGE_VERSION_FAILURE) Image version embedded in header is less than version of currently running image and update rejected
* @value(StatusCode_INVALID_SECTION_KEY) The supplied firmware update image has a different section key than what is associated with the application currently running on the device
* @value(StatusCode_IMAGE_VERIFY_FAILURE) Response after the completely written firmware image verification has failed
* @value(StatusCode_INVALID_STATE) Response to an API called in an invalid state, e.g. supplying more data when waiting for reboot
* @value(StatusCode_INVALID_ORDER) Supplied data with incorrect order for the current state
* @value(StatusCode_TOO_FEW_BYTES) Supplied first data packet with less than minimum required bytes
* @value(StatusCode_PARSER_ERROR) Update container format parser has encountered an unrecoverable error in the byte stream
*/
typedef enum
{
    SE_PATCH_StatusCode_NONE,
    SE_PATCH_StatusCode_COMPLETED,
    SE_PATCH_StatusCode_INVALID_ARG,
    SE_PATCH_StatusCode_INVALID_PATCH_IMAGE,
    SE_PATCH_StatusCode_INVALID_SOURCE_IMAGE,
    SE_PATCH_StatusCode_INVALID_TARGET_IMAGE,
    SE_PATCH_StatusCode_INVALID_PATCH_TAG,
    SE_PATCH_StatusCode_IMAGE_TOO_LARGE,
    SE_PATCH_StatusCode_IMAGE_TOO_SMALL,
    SE_PATCH_StatusCode_SECTION_NOT_AVAILABLE,
    SE_PATCH_StatusCode_SECTION_ERASE_FAILURE,
    SE_PATCH_StatusCode_SECTION_WRITE_FAILURE,
    SE_PATCH_StatusCode_IMAGE_VERSION_FAILURE,
    SE_PATCH_StatusCode_INVALID_SECTION_KEY,
    SE_PATCH_StatusCode_IMAGE_VERIFY_TAG_FAILURE,
    SE_PATCH_StatusCode_IMAGE_VERIFY_ALG_FAILURE,
    SE_PATCH_StatusCode_IMAGE_DECRYPT_FAILURE,
    SE_PATCH_StatusCode_INVALID_STATE,
    SE_PATCH_StatusCode_INVALID_ORDER,
    SE_PATCH_StatusCode_TOO_FEW_BYTES,
    SE_PATCH_StatusCode_PARSER_ERROR,
    SE_PATCH_StatusCode_DECRYPTION_ERROR,
    SE_PATCH_StatusCode_INSTALL_ERROR,
    SE_PATCH_StatusCode_FLASH_ERROR,
    SE_PATCH_StatusCode_FLASH_SEGMENT_ERROR,
    SE_PATCH_StatusCode_FLASH_CIPHER_ERROR,
    SE_PATCH_StatusCode__MAX__
}  SE_PATCH_StatusCode;


/*!
 * High-level AMDM image types.
 *
 * These are the types of firmware images that may be presented to the Update module.
 */
typedef enum
{
    SE_PATCH_ImageType_NONE = 0,
    SE_PATCH_ImageType_APP
}  SE_PATCH_ImageType;



/*! Set the delay type to COMMAND to specify rebooting upon command.
 *  The application is responsible for marking the update as "ready to install".
*/
#define SE_PATCH_RebootDelay_COMMAND         ((uint32_t)0xFFFF)

/*! Set the delay type to IMMEDIATE to specify rebooting and installing immediately.
*/
#define SE_PATCH_RebootDelay_IMMEDIATE       ((uint32_t)0)

/*! Set the delay type to NEXT to specify installation on next reboot.
 * The user application is still responsible for initiating the reboot.
*/
#define SE_PATCH_RebootDelay_NEXT            ((uint32_t)1)

/*!
* Update start setup data structure.
*
* @field(type) Target update location of firmware image presented to Update module.
*              This field may be set if known, or may be omitted (set to NONE) to use the firmware update image's
*              embedded type determined on-the-fly.
* @field(rebootDelay) Specify the reboot delay that is to occur after a completed firmware update.
*                     @p(blist)
*                     - RebootDelay_IMMEDIATE  reboot immediately upon successful written image verification.
*                     - 1 to 0xFFFE random delay, in seconds, selected from within this window before rebooting as if RebootDelay_IMMEDIATE was selected.
*                     - RebootDelay_COMMAND wait indefinately upon successful written image verification.
*                       The user is responsible for rebooting the system, e.g. by calling {@link fm.driver.System#reset}.
*                     @p
* @field(totalLength) Provide if the image length is known - only used to initially reject an update if it is too large
*                     for the device before examining the actual header. Set to 0 to ignore this first check and use the
*                     embedded image header length in a subsequent {@link #data} call.  The type must also be specified
*                     (not ImageType_NONE) to be able to validate this length parameter.
*/
typedef struct
{
    SE_PATCH_ImageType type;
    uint16_t rebootDelay;
    uint32_t totalLength;
}  SE_PATCH_StartInfo;

/*!
* Status reporting enumeration indicating the current stage of
* the update process.
*
* @value(Stage_IDLE) Updater is idle and awaiting a start command.
* @value(Stage_UPDATE) Updater is actively processing data commands.
* @value(Stage_VERIFIED) Updater has finished update and written a valid image
*                        to non-volatile storage that is ready to be run on the
*                        next reboot.
*/
typedef enum
{
    SE_PATCH_Stage_IDLE,
    SE_PATCH_Stage_UPDATE,
    SE_PATCH_Stage_VERIFIED
}  SE_PATCH_Stage;

/*!
* Command response structure.
*
* There are different semantics to the completed flag depending on how it
* is obtained (as API result or through {@link #poll}).
*
* If this status is polled for at any time after an update has successfully completed
* but the system has not yet restarted, the `completed` flag is set, the `accumBytes` records
* the total bytes recorded in the image, and the `stage` will be VERIFIED.
*
* If this status is obtained as an output from an API call, the `completed` flag is set to
* indicate the API call completed.
*
* The accumBytes and totalBytes fields are useful as a progress indicator where
* percentage could be calculated as (accumBytes * 100) / totalBytes. 
*
* @field(completed) Set to indicate completion of the specified operation.
* @field(error) Set if an error has occured.  An error will result in the stage set to IDLE.
* @field(code) Current status code.
* @field(stage) Set to the updater's current stage at time of generation of this message.
* @field(accumBytes) Records the number of patch bytes received (excluding metadata).
* @field(totalBytes) Records the total number of patch bytes expected (excluding metadata).
*/
typedef struct 
{
    bool completed;
    bool error;
    SE_PATCH_StatusCode code;
    SE_PATCH_Stage stage;
    uint32_t accumBytes;
    uint32_t totalBytes;
} SE_PATCH_Status;


/*!
* Initialize a Status structure before using it.
*/
void SE_PATCH_InitStatus(SE_PATCH_Status* status);

/*! 
 * Helper to print the status.
 */
void SE_PATCH_PrintStatus(SE_PATCH_Status* status);

/*!
* Starts a firmware update.
*
* This call must be followed up by a {@link #data} or {@link #abort} call provided it
* returns TRUE.
*
* @param(info) Firmware update start parameters.
* @param(status) Supplied structure to be filled in with detailed API result status.
*
* @Note If info.rebootDelay is SE_PATCH_RebootDelay_COMMAND, then user must call SE_PATCH_InstallAtNextReset()
*       to mark image for installation at next reset.  Otherwise, patch engine will do this.
*
* @return TRUE if the update start request was accepted and the update process
*         is awaiting data.
*         FALSE if the update start request was rejected for one of these
*         failures:
*         @p(blist)
*            - ImageType was set to a type other than NONE and
*                total length is too large for the section allocated to the requested application type.
*            - Invalid image type, including `ImageType_BOOT` which is not supported for update.
*            - Invalid state.  Start can only be initiated when the update stage is IDLE.
*              An {@link #abort} is required before restarting an update in-progress.
*         @p
*/
SE_ErrorStatus SE_PATCH_Init(SE_PATCH_Status* p_PatchStatus, const SE_PATCH_StartInfo* p_StartInfo);

/*!
* Supply a portion of a stream of data to the firmware patching engine.
*
* This function blocks until the operation is completed which may consist of one or both of:
* @p(blist)
*    - Writing the data to flash.
*    - Erasing flash sectors.
* @p
*
* No action is taken against the non-volatile storage unless the provided
* data was verified to contain the start of a valid firmware image.
*
* There is a requirement for data ordering - the first
* {@link #getMinUpdateImageDataLen} bytes must be sent first and available as a unit
* to the `data` function.  These bytes contain enough information for the updater
* to make a decision on whether to proceed.  All subsequent bytes of the
* firmware update image must also be delivered in order.
*
* Additionally, the count of bytes is accumulated until the expected number
* of bytes is received, at which time the written firmware image will be fully verified.
* There is no protection against duplicate data packets.
*
* @param(status) Supplied structure to be filled in with detailed API result status.
* @param(data) Pointer to firmware image data buffer
* @param(len) Length of firmware update image data in buffer
*
* @return TRUE - data was accepted.
*         FALSE - error accepting data, see status.
*           On the first data submission, the update image can be rejected
*           with the following errors:
*               @p(blist)
*               - StatusCode_IMAGE_VERSION_FAILURE
*               - StatusCode_INVALID_IMAGE
*               - StatusCode_INVALID_SECTION_KEY
*               - StatusCode_IMAGE_TOO_LARGE
*               -   More...
*               @p
*
*/
SE_ErrorStatus SE_PATCH_Data(SE_PATCH_Status* status, const uint8_t* data, uint32_t len );


/*!
 * Mark a downloaded update file as "ready to install".  
 *
 * Until the update is explicitly marked as such, the bootloader will ignore it!
 *
 * This feature allows for control when the actual installation is performed, 
 * not just on the next reset after downloading.
 *
 * Note: To have the patch engine automatically mark the update as "ready to install"
 *       use the initialization parameter: SE_PATCH_RebootDelay_NEXT.
 *       To have the patch engine automatically mark the update as "ready to install"
 *       *and* immediately reboot, use the initialization parameter: SE_PATCH_RebootDelay_IMMEDIATE.
 *
 * @Return SUCCESS if the image was marked, false otherwise.
 */
SE_ErrorStatus SE_PATCH_InstallAtNextReset(SE_PATCH_Status* status);


/*!
* Abort the update in progress.  Return the state machine to IDLE.
*
* If necessary, abort will cause the firmware update image that was written to the
* current update section to be invalidated before returning.
*
* This is a blocking call and may involve non-volatile write or erase operations.
*
* Abort will always return the updater state to IDLE.  However, errors invalidating
* the non-volatile memory can be detected by inspecting the returned status codes:
*      @p(blist)
*           - StatusCode_SECTION_ERASE_FAILURE: could not invalidate image.
*                   if an image was successfully written, upon next reboot it will be
*                   booted, but only if it verifies successfully by the bootloader
*                   (otherwise the currently running firmware image is booted again).
*      @p
* @param(status) Supplied structure to be filled in with detailed API result status.
*
* @return SUCCESS if the abort completed, ERROR otherwise.
*/
SE_ErrorStatus SE_PATCH_Abort(SE_PATCH_Status* status);


/*!
* Get the current update status.
*
* Fill in the provided status structure.
* The completed flag is set only when the update image has been written
* to flash and verified, and the device has not rebooted yet.
*
* The error flag and status codes are set according to the result of the
* last API call.
*
* @param(status) Supplied structure to be filled in with detailed API result status.
*
* @return SUCCESS if the status was returned in the provided structure, ERROR otherwise.
*/
SE_ErrorStatus SE_PATCH_Poll(SE_PATCH_Status* status);


/*!
* Get a string discription of the specified status code.
* Return string, or empty string if code has no string
* or strings no compiled in.
*/
const char* SE_PATCH_GetStatusCodeString(SE_PATCH_StatusCode code);



#define SE_TAG_LEN              (32)  /* SHA-256 hash of FW image */


/**
 * @brief  Firmware Information structure definition.
 *         This structure is used to retrieve some information
 *         about the active Firmware.
 */
typedef struct
{
    uint32_t ActiveFwVersion;            /*!< Firmware version (see @ref SFU_FW_VERSION_START_NUM for the min. valid value) */
    uint32_t ActiveFwSize;               /*!< Firmware size (bytes) */
    uint8_t  ActiveFwTag[SE_TAG_LEN];    /*!< Firmware Tag*/
} SE_APP_ActiveFwInfo;

/* Extract version components "major", "minor" and "patch" from the 32-bit version field.
 * The version field should contain a value formatted such that major is the high bytes; minor is the middle short and
 * patch is the low byte.
 * Without any explicit formatting of this field, the version numbers will simply ramp
 * patch from 0 to 255 then minor from 0-65535 then major from 0-255.
 * E.g. a version of "452" would show as "0.1.196".
 * Note that any use of version field within the bootloader (e.g. anti-rollback feature) is
 * not impacted by specific formatting as long as a versions are always incrementing,
 * e.g. v1.12.0 is considered greater than v0.15.1
 */
#define FW_VERSION_MAJOR(x) (((uint32_t)(x) >> 24) & 0x000000FF)
#define FW_VERSION_MINOR(x) (((uint32_t)(x) >>  8) & 0x0000FFFF)
#define FW_VERSION_PATCH(x) (((uint32_t)(x) >>  0) & 0x000000FF)

SE_ErrorStatus SE_APP_GetActiveFwInfo(SE_StatusTypeDef* peSE_Status, SE_APP_ActiveFwInfo* p_FwInfo);
SE_ErrorStatus SE_APP_GetSecureUserData(SE_StatusTypeDef* peSE_Status, void* p_Data, uint32_t len);


