# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps

import sys
import os
from django.conf import settings
from django.template import Context, loader

project_path = "/Users/miquel/UN/0003-CRPTDEV/crppdmt/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crppdmt.settings'

import django
django.setup()

from crppdmt.my_ftp import MyFTP
from crppdmt.my_mail import MyMail
from crppdmt.models import ExpertRequest

def test_ftp():
    my_FTP = MyFTP()
    my_FTP.upload_file("TEST.txt", "TEST_DIR", "TEST.txt")
    my_FTP.download_file("TEST_DIR", "TEST.txt", "TESTOS.txt")

def test_mail():
    try:
        my_mail = MyMail()
        subject = "DMT - New Expert Request to Validate"
        html_template = loader.get_template('crppdmt/email/supervisor.html')
        html_content = html_template.render(Context({'request_name': "REQ_NAME",}))
        text_template = loader.get_template('crppdmt/email/supervisor.txt')
        text_content = text_template.render(Context({'request_name': "REQ_NAME",}))
        recipients = ["miguel.corral@gmail.com"]
        if 1 == 1:
            recipients = recipients + ["miguel.corral@cityresilience.org"]
            print("Recipients: " + str(recipients))
        #my_mail.send_mail(subject, html_content, text_content, recipients)
    except:
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass

def test_expert_request():
    expert_request = ExpertRequest.objects.get(id=48)
    print str(expert_request.has_no_empty_text_fields())




if __name__ == "__main__":
    #test_ftp()
    #test_mail()
    test_expert_request()

