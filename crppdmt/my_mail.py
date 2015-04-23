import sys
from django.core.mail import EmailMultiAlternatives
from crppdmt.settings import EMAIL_HOST_USER, BASE_DIR
from easy_pdf.rendering import render_to_pdf


class MyMail():

    def __init__(self):
        pass

    @staticmethod
    def send_mail(subject, html_content, text_content, recipients, expert_request, attach_tor=False, attach_letter=False):

        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, recipients)

        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'

        # attachments stuff
        if attach_letter or attach_tor:
            context = {'expert_request': expert_request, 'pagesize': 'A4', 'BASE_DIR': BASE_DIR, }
            try:
                tor_pdf = render_to_pdf('crppdmt/tor.html', context)
                letter_pdf = render_to_pdf('crppdmt/letter_of_request.html', context)
                msg.attach('ToR.pdf',tor_pdf,'application/pdf')
                msg.attach('LetterOfRequest.pdf',letter_pdf,'application/pdf')
            except:
                print("Error attaching ToR and Letter to Email. Request: " + expert_request.name)
                print("Error: " + str(sys.exc_info()))

        msg.send()
