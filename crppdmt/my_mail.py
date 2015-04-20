from django.core.mail import EmailMultiAlternatives
from crppdmt.settings import EMAIL_HOST_USER


class MyMail():

    def __init__(self):
        pass


    def send_mail(self, subject, html_content, text_content, recipients, attachments=None):

        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, recipients)

        msg.attach_alternative(html_content, "text/html")
        msg.mixed_subtype = 'related'

        if attachments is not None:
            for attachment in attachments:
                msg.attach(attachment.name, attachment.read(), attachment.content_type)


        msg.send()
