# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps

import sys
import os
import hashlib
from django.conf import settings
from django.template import Context, loader
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf

project_path = "/Users/miquel/UN/0003-CRPTDEV/crppdmt/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crppdmt.settings'

import django
django.setup()

from crppdmt.settings import BASE_DIR

from crppdmt.my_ftp import MyFTP
from crppdmt.my_mail import MyMail
from crppdmt.models import ExpertRequest
from crppdmt.settings import NORCAP_EMAILS, SECONDMENTS_MAIL_LIST, NORCAP_FOCAL_POINTS
from crppdmt.constants import PROFILE_SHELTER

def test_ftp():
    my_FTP = MyFTP()
    my_FTP.upload_file("Calendari2015.pdf", "mai.mani", "Calendari2015.pdf")
    #my_FTP.download_file("TEST_DIR", "TEST.txt", "TESTOS.txt")

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


def test_render_to_pdf():
        expert_request = ExpertRequest.objects.get(id=11)
        context = {'expert_request': expert_request,
           'pagesize': 'A4',
           'BASE_DIR': BASE_DIR,
        }
        #tor_template = loader.get_template('crppdmt/tor.html')
        #letter_template = loader.get_template('crppdmt/letter_of_request.html')
        tor_pdf = render_to_pdf('crppdmt/pdf/tor.html', context)
        tor_file = open("tor_file.pdf",'w')
        tor_file.write(tor_pdf)
        tor_file.close()

        #letter_pdf = render_to_pdf('crppdmt/letter_of_request.html', context)


def test_encryption():
    # encrypt password
    print(hashlib.sha224("password").hexdigest());


def test_NORCAP_emails():
    print("SHELTER: " + NORCAP_EMAILS[PROFILE_SHELTER])
    print("SHELTER: " + NORCAP_FOCAL_POINTS[PROFILE_SHELTER])
    print("SECONDMENTS_MAIL_LIST[0]: " + SECONDMENTS_MAIL_LIST[0])



if __name__ == "__main__":
    test_ftp()
    #test_mail()
    #test_expert_request()
    #test_render_to_pdf()
    #test_encryption()
    #test_NORCAP_emails()

