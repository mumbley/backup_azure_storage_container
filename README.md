# Blob Archiver
*** Note ***
Due to features in the Azure SDK, this code was replaced by the Golang version [in one of my other repos](https://github.com/mumbley/asma-async)
This works well enough but, in the particular case this was written to solve (6m files of various sizes, some < 1KB, the facilities provided by the Azure SDK, along with some deliberate throttling, meant that something else was required. There is some information about the issue in the other repo's README.md

The **Blob Archiver** Python class provides tools to manage Azure Blob Storage containers:
- Archive blobs from an Azure container into a tar file (with optional compression).
- Upload tar archives back to Azure Storage.
- Copy the tar archive to a destination container.
- Delete blobs from a container.
- Remove locally created tar archive files.
## Features

-  **Stream Blobs to Tar**: Archive blobs from an Azure container into a tar/tgz file.
-  **Upload**: Extract and upload files from a tar/tgz archive to an Azure container.
-  **Copy Archive to a Storage Container**: Upload the tar archive to another Azure container.
-  **Delete Blobs**: Remove all blobs from an Azure container.
-  **Clean Up Archive**: Delete the local tar archive.
---
## Class Input Variables
The following variables are required:
|variable|type|default|description|
|--|--|--|--|
|connection_string|string||Storage Account access key. This can be found in the Azure console under storage container -> Networking + Security -> Access Keys|
|container_name|string||Name of the Azure container in the storage account|
|compression|bool|None|Compress the tar archive|
|path|path|None|Path to save the archive file on the local host|
|tarfile_name|string|None|If unset, the name defaults to the format `<container_name>-<DD-MM-YYYY>-<.tar/.tgz>`|
 |overwrite|bool|True|Overwrite existing files on the storage container|
 |destination_connection_string|string|None|Storage Account access key for the archive destination. Required if yoou want to store your tar file in a storage container. This can be found in the Azure console under storage container -> Networking + Security -> Access Keys.|
|destination_container_name|string|None|Container in the destination Storage Account

## Class Defaults
The following variables are set, depending on the variables passed to a class instance and defaults:
|variable|rule|description|
|--|--|--|
str_time|set to `datetime.now().strftime("%d-%m-%Y")`|Used for setting timestamps on the default tarfile name and the destination container folder|
|write_mode|adds a `gz` flag if `compression` is set to `True`|Compresses the tarfile. The tarfile suffix will be `.tgz`|
|read_mode|adds a `gz` flag if `compression` is set to `True`|Required for reading a compressed tarfile|
|destination_file_suffix|default is `.tar`, set to `.tgz` if `compression` is set to `True`|Notifies a user if the tarfile is compressed
|destination_container_path|set to `datetime.now().strftime("%d-%m-%Y")`|In this version, this is statically set to the date of the archive|

Note the current setting for the destination blob overwrite is hard coded to `False`
