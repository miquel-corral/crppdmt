import sys
import os
from django.core.mail import EmailMultiAlternatives
from crppdmt.settings import EMAIL_HOST_USER, BASE_DIR, SMT_URL
from crppdmt.settings_private import SECONDMENTS_MAIL_LIST, NORCAP_FOCAL_POINTS
from easy_pdf.rendering import render_to_pdf


class MyMail():

    def __init__(self):
        pass

    @staticmethod
    def send_mail(subject, html_content, text_content, recipients, expert_request=None, attach_tor=False,
                  attach_letter=False):

        # control of environment
        deploy_env = os.environ.get('DEPLOY_ENV','LOCAL')
        if "HEROKU" != deploy_env:
            # local env email only to secondments mail list
            recipients = SECONDMENTS_MAIL_LIST
            # subject with TEST
            subject = "This is a TEST email! " + subject
            # test indicator to render PDF as test sample
            test = True

        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, recipients, bcc=SECONDMENTS_MAIL_LIST)

        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'

        # attachments stuff
        if attach_letter or attach_tor:
            context = {'expert_request': expert_request, 'pagesize': 'A4', 'BASE_DIR': BASE_DIR, 'test_env': test,
                       'SMT_URL': SMT_URL, 'NORCAP_FOCAL_POINT': \
                        NORCAP_FOCAL_POINTS[expert_request.expert_profile_type],
                       'SECONDMENTS_EMAIL': SECONDMENTS_MAIL_LIST[0]}
            try:
                tor_pdf = render_to_pdf('crppdmt/pdf/tor.html', context)
                letter_pdf = render_to_pdf('crppdmt/pdf/letter_of_request.html', context)
                msg.attach('ToR.pdf',tor_pdf,'application/pdf')
                msg.attach('LetterOfRequest.pdf',letter_pdf,'application/pdf')
            except:
                print("Error attaching ToR and Letter to Email. Request: " + expert_request.name)
                print("Error: " + str(sys.exc_info()))

        msg.send()
