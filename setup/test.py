# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps

import sys
import os
from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/crppdmt/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crppdmt.settings'

import django
django.setup()

from crppdmt.my_ftp import MyFTP
from crppdmt.my_mail import MyMail

def test_ftp():
    my_FTP = MyFTP()
    my_FTP.upload_file("TEST.txt", "TEST_DIR", "TEST.txt")
    my_FTP.download_file("TEST_DIR", "TEST.txt", "TESTOS.txt")

def test_mail():
    my_mail = MyMail()
    my_mail.send_mail("SUBJECT", "<strong>HTML TEXT</strong>", "PLAIN TEXT", ["miguel.corral@cityresilience.org"], None)

if __name__ == "__main__":
    #test_ftp()
    test_mail()

