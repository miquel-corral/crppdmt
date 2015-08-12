import os
from crppdmt.my_ftp import *

############################################################
#
# Helper functions to manage documents
#
#############################################################


def upload_file(remote_folder, document_name):

    # remove document in local file system
    try:
        ret = 0
        print("FTP. document_name: " + document_name)

        my_ftp = MyFTP()
        ret = my_ftp.upload_file(document_name, remote_folder, document_name)

        os.remove(document_name)
        return ret
    except:
        print("Error uploading project file: " + document_name)
        print(sys.exc_info())
    finally:
        return ret


def get_ftp_file_content(remote_folder, remote_file):
    file_content = None
    try:
        my_ftp = MyFTP()
        file_content = my_ftp.get_binary_file(remote_folder, remote_file)
    except:
        print("Error getting ftp file: " + remote_file)
        pass  # silent remove
    finally:
        return file_content


