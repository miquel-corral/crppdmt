import sys
from ftpretty import ftpretty
from settings_private import *



class MyFTP():

    def __init__(self):
        pass

    def upload_file(self, local_file_path, remote_folder, remote_file_name):
        try:
            # open connection
            f = ftpretty(FTP_HOST, FTP_USER, FTP_PASS)
            # cd base folder
            f.cd(FTP_BASE_DIR)
            # put the file
            f.put(local_file_path, remote_folder + "/" + remote_file_name)
        except:
            print("Unexpected error:", sys.exc_info())
        finally:
            if f:
                f.close()


    def download_file(self, remote_folder, remote_file_name, local_file_path):
        try:
            # open connection
            f = ftpretty(FTP_HOST, FTP_USER, FTP_PASS)
            # cd base folder
            f.cd(FTP_BASE_DIR)
            # download the file
            contents = f.get(remote_folder + "/" + remote_file_name)
            my_file = open(local_file_path, 'wb')
            my_file.write(contents)
            my_file.close()
        except:
            print("Unexpected error:", sys.exc_info())
        finally:
            if f:
                f.close()

    def get_binary_file(self,remote_folder, remote_file_name):
        contents = None
        try:
            # open connection
            f = ftpretty(FTP_HOST, FTP_USER, FTP_PASS)
            # cd base folder
            f.cd(FTP_BASE_DIR)
            # download the file
            contents = f.get(remote_folder + "/" + remote_file_name)
        except:
            print("Unexpected error:", sys.exc_info())
        finally:
            if f:
                f.close()
            return contents
