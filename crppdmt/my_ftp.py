import sys
from django.conf import settings
from ftplib import FTP

# FTP Details
FTP_HOST = "citiresilience.org"
FTP_USER = "citiresilience"
FTP_PASS = "Mike2003"
FTP_PORT = 21
BASE_DIR = "crppdmtfiles"


class MyFTP():

    ftp = FTP()

    def __init__(self):
        pass

    def connect(self, server, ftp_user, ftp_password, port):
        """
        Connects the remote host to the server from the information provided to the connect method.
        If the connection is successful, the messaged will logged and displayed in the console, otherwise
        Exception is raised with the error displayed to the console and program execution halts.
        :param server: The address of the server
        :param ftp_user: The FTP user id.
        :param ftp_password: The FTP password.
        :param port: The port number.
        """
        try:
            self.ftp.connect(server, port)
            self.ftp.login(user=ftp_user, passwd=ftp_password)
        except:
            print("Unexpected error:", sys.exc_info())

    def make_directory(self, directory):
        """
        Creates the new directory in the connected server in the root or in the directory specified via the parameter.
        :param directory: Directory name to create.
        """
        try:
            self.ftp.mkd(directory)
        except:
            print("Unexpected error:", sys.exc_info())

    def change_directory(self, directory):
        """
        CD's into the directory of our wish by providing the directory name as the parameter to it.
        :param directory: Directory name to change to it.
        """
        try:
            self.ftp.cwd(directory)
        except:
            print("Unexpected error:", sys.exc_info())

    def directory_exists(self, directory_name):
        """
        Checks if the directory you are trying to upload the files is already present or not and if
        its already present CD's into the directory and if not, creates the directory and CD's into the
        newly created directory.
        :param directory_name: Directory name to check its existence.
        """
        try:
            new_dir_name = directory_name.strip("/")
            if new_dir_name in self.ftp.nlst():
                self.change_directory(directory_name)
            else:
                self.make_directory(directory_name)
                self.change_directory(directory_name)
        except:
            print("Unexpected error:", sys.exc_info())

    def get_directory_listing(self):
        """
        Lists all the contents in the connected server or in the specified folder in the server.
        """
        data = []
        self.ftp.dir(data.append)
        for line in data:
            print("-", line)

    def upload_file(self, filename):
        """
        The file provided with filename will be uploaded to the server in the recommended
        format automatically to the desired directory.
        :param filename: Name of the file to upload.
        """
        try:
            if filename.lower().endswith(('.*')):
                with open(filename, 'r') as f:
                    self.ftp.storlines('STOR {}'.format(filename), f)
            else:
                with open(filename, 'rb') as f:
                    self.ftp.storbinary('STOR {}'.format(filename), f)
        except:
            print("Unexpected error:", sys.exc_info())

    def download_file(self, filename):
        """
        Downloads the file from the connected server, provided the name is passes as the parameter.
        :param filename: Name of the file to download.
        """
        try:
            self.ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
        except:
            print("Unexpected error:", sys.exc_info())


    def close(self):
        """
        Closes the FTP connection.
        """
        try:
            self.ftp.close()
        except:
            print("Unexpected error:", sys.exc_info())

    def upload_project_file(self, request_name, file_name):
        try:
            # connect to the server
            self.connect(FTP_HOST, FTP_USER, FTP_PASS, FTP_PORT)
            print("Connected")
            # move to base directory
            self.change_directory(BASE_DIR)
            print("change_directory")
            # create and change directory
            self.directory_exists(request_name)
            print("change_directory")
            # upload the file
            print("uploading file: " + settings.BASE_DIR + "/" + file_name)
            self.upload_file("./" + file_name)
            print("upload_file")
        except:
            print("FTP Unexpected error:", sys.exc_info())
        finally:
            # disconnect from the server
            self.close()




