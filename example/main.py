from src import archive_blob
import os
from datetime import datetime 
class Main():
    def __init__(self):
        self.destination_path = '/tmp/foo'
        self.destination_file_suffix = 'tgz'
        self.write_mode = "w"
        self.read_mode = "r"
        self.compression = False
        self.connection_string = "<changeme>"
        #self.connection_string = "<changeme>"
        self.container_name = '<changeme>'
        #self.container_name = <changeme>'
        self.str_time = datetime.now().strftime("%d-%m-%Y")
        self.file_string = self.container_name + '-' + self.str_time + '.' + self.destination_file_suffix
        self.tar_file = os.path.join(self.destination_path, self.file_string)
        self.overwrite_existing_files = True
        self.destination_connection_string = "<changeme>"
        #self.destination_connection_string = "<changeme>"
        self.destination_container_name = '<changeme>'
        #self.destination_container_name = '<changeme>'
    
    def run(self):
        archiver = archive_blob.Blob_archiver(container_name=self.container_name, 
            connection_string=self.connection_string,
            compression=self.compression,
            path='/Users/stevegall/dev/python/dev/azure-backup/src/',
	    destination_connection_string=self.destination_connection_string,
            destination_container_name=self.destination_container_name)
            
        archiver.stream_blobs_to_tar()
        #archiver.delete_all_blobs()
        #archiver.upload_tar_content_to_azure()
        #archiver.delete_tar_archive_file()
        archiver.copy_archive_to_storage_container()

if __name__ == '__main__':
    main = Main()
    main.run()
