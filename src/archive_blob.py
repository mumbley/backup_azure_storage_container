from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os 
import tarfile
from datetime import datetime

class Blob_archiver:
    
    def __init__(
            self, 
            connection_string, 
            container_name, 
            compression=None, 
            path=None, 
            tarfile_name=None,
            overwrite=True, 
            destination_connection_string=None,
            destination_container_name=None
        ):
        
        self.connection_string = connection_string
        self.container_name = container_name
        self.compression = compression
        self.path = path
        self.tarfile_name = tarfile_name
        self.str_time = datetime.now().strftime("%Y-%m-%d")
        self.overwrite_existing_files = overwrite
        self.destination_connection_string = destination_connection_string
        self.destination_container_name = destination_container_name
        

    @property
    def write_mode(self):
        return 'w:gz' if self.compression == True else "w"
    @property
    def read_mode(self):
        return 'r:gz' if self.compression == True else "r"
    @property
    def destination_file_suffix(self):
        return '.tgz' if self.compression == True else '.tar'
    @property
    def tar_file(self):
        return self.container_name + '-' + self.str_time + self.destination_file_suffix if self.tarfile_name == None else self.tarfile_name
    @property
    def blob_service_client(self):
        return BlobServiceClient.from_connection_string(self.connection_string) 
    @property
    def container_client(self):
        return self.blob_service_client.get_container_client(self.container_name)
    @property
    def destination_blob_service_client(self):
        return BlobServiceClient.from_connection_string(self.destination_connection_string)
    @property
    def destination_container_client(self):
        return self.destination_blob_service_client.get_container_client(self.destination_container_name) if self.destination_blob_service_client != None else None
    @property
    def destination_container_path(self):  
        return f"{self.str_time}/{self.container_name}"
    
    def copy_archive_to_storage_container(self):
        with open(self.tar_file, 'rb') as tar:
            blob_name = f"{self.str_time}/{self.container_name}/{self.tar_file}"
            blob_client = self.destination_container_client.get_blob_client(blob=blob_name)
            blob_client.upload_blob(data=tar, overwrite=False)
            print(f"Uploaded {self.tar_file} to Azure Storage container {self.destination_container_name}")

    def stream_blobs_to_tar(self):      
        if self.path and not os.path.exists(self.path):
            os.makedirs(self.path)
        with tarfile.open(self.tar_file, self.write_mode) as tar:
            for blob in self.container_client.list_blobs():
                blob_name = blob.name
                print(f"Adding blob: {blob_name}")

                blob_client = self.container_client.get_blob_client(blob_name)
                stream = blob_client.download_blob()

                tarinfo = tarfile.TarInfo(name=blob_name)
                tarinfo.size = blob.size
                tar.addfile(tarinfo, fileobj=stream)

        print(f"Blobs have been archived to {self.tar_file}")

    def upload_tar_content_to_azure(self):
        with tarfile.open(self.tar_file, self.read_mode) as tar:
            for tarinfo in tar:
                if tarinfo.isreg():
                    file_obj = tar.extractfile(tarinfo)
                    if file_obj is not None:
                        blob_client = self.container_client.get_blob_client(blob=tarinfo.name)
                        blob_client.upload_blob(file_obj, overwrite=self.overwrite_existing_files)
                        print(f"Uploaded {tarinfo.name} to Azure Storage container {self.container_name}")

        print(f"All files have been uploaded to the Azure container {self.container_name}")
        
    def delete_all_blobs(self):
        for blob in self.container_client.list_blobs():
            blob_name = blob.name
            print(f"Deleting blob: {blob_name}")
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

    def delete_tar_archive_file(self):
        try:
            os.remove(self.tar_file)
        except FileNotFoundError:
            print(f"unable to remove file - file [{self.tar_file}] not found")
        except:
            print(f"unable to delete file")

