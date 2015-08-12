from django.template import loader, Context
from crppdmt.settings import *
from crppdmt.my_mail import *
from crppdmt.trace import *
from crppdmt.models import ExpertRequest

def send_user_validation_email(person, rejection_reason=None):
    try:
        if rejection_reason:
            rejected = True
        else:
            rejected = False

        my_mail = MyMail()
        recipients = [person.email]
        if rejected:
            subject = "SMT - User Registration Rejected"
            html_template = loader.get_template('crppdmt/email/user_rejected.html')
            html_content = html_template.render(Context({'person': person, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/user_rejected.txt')
            text_content = text_template.render(Context({'person': person, 'SMT_URL': SMT_URL}))
            action = MAIL_USER_REJECTED
        else:
            subject = "SMT - User Registration Validated"
            html_template = loader.get_template('crppdmt/email/user_validated.html')
            html_content = html_template.render(Context({'person': person, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/user_validated.txt')
            text_content = text_template.render(Context({'person': person, 'SMT_URL': SMT_URL}))
            action = MAIL_USER_VALIDATED

        my_mail.send_mail(subject, html_content, text_content, recipients)

        # trace after email sent
        trace_action(MAIL_USER_REJECTED, None, person)

    except:
        print("Error sending user validated email. Person:" + person.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass


def send_new_expert_email(person, supervisor):
    try:
        my_mail = MyMail()
        recipients = [supervisor.email, person.email]
        subject = "SMT - New Expert Registered"
        html_template = loader.get_template('crppdmt/email/user_registered.html')
        html_content = html_template.render(Context({'person': person, 'supervisor':supervisor, 'SMT_URL': SMT_URL}))
        text_template = loader.get_template('crppdmt/email/user_registered.txt')
        text_content = text_template.render(Context({'person': person, 'supervisor':supervisor, 'SMT_URL': SMT_URL}))
        my_mail.send_mail(subject, html_content, text_content, recipients)
        trace_action(MAIL_EXPERT_REGISTERED, None, person)

    except:
        print("Error sending new expert registration email. Person:" + person.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass

def send_expert_message_email(expert_message, person, expert_request):
    try:
        my_mail = MyMail()
        recipients = SECONDMENTS_MAIL_LIST
        subject = "SMT - " + expert_message.subject
        html_template = loader.get_template('crppdmt/email/expert_message.html')
        html_content = html_template.render(Context({'person': person, 'expert_message': expert_message, 'SMT_URL': SMT_URL}))
        text_template = loader.get_template('crppdmt/email/expert_message.txt')
        text_content = text_template.render(Context({'person': person, 'expert_message': expert_message, 'SMT_URL': SMT_URL}))

        # check if expert_request_id is set
        if expert_request:
            recipients = recipients + [expert_request.supervisor]

        my_mail.send_mail(subject, html_content, text_content, recipients)

        trace_action(MAIL_EXPERT_REGISTERED, expert_request, person)

    except:
        print("Error sending new expert registration email. Person:" + person.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass

def send_user_registration_email(person, certifier):
    try:
        my_mail = MyMail()
        recipients = [certifier.email, person.email]
        subject = "SMT - New User Registered"
        html_template = loader.get_template('crppdmt/email/user_registered.html')
        html_content = html_template.render(Context({'person': person, 'certifier':certifier, 'SMT_URL': SMT_URL}))
        text_template = loader.get_template('crppdmt/email/user_registered.txt')
        text_content = text_template.render(Context({'person': person, 'certifier':certifier, 'SMT_URL': SMT_URL}))
        my_mail.send_mail(subject, html_content, text_content, recipients)
        trace_action(MAIL_USER_REGISTERED, None, person)

    except:
        print("Error sending user registration email. Person:" + person.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass


def send_request_email_to(expert_request, action):
    try:
        my_mail = MyMail()
        recipients = [expert_request.supervisor.user.email]

        if action == MAIL_REQUEST_TO_REVIEW:
            subject = "SMT - New Expert Request to Review"
            html_template = loader.get_template('crppdmt/email/review.html')
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/review.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.supervisor is not expert_request.request_creator:
                recipients = recipients + [expert_request.request_creator.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)

        if action == MAIL_REQUEST_TO_CERTIFY:
            subject = "SMT - New Expert Request to Certify"
            html_template = loader.get_template('crppdmt/email/certify.html')
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/certify.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.country_representative is not expert_request.supervisor:
                recipients = recipients + [expert_request.country_representative.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)

        if action == MAIL_REQUEST_CERTIFIED:
            subject = "UN-HABITAT - New Expert Request"
            html_template = loader.get_template('crppdmt/email/certified.html')
            html_content = html_template.render(Context({'expert_request': expert_request,
                                        'NORCAP_FOCAL_POINT': NORCAP_FOCAL_POINTS[expert_request.expert_profile_type.name.strip()],
                                        'SMT_URL': SMT_URL, 'SECONDMENTS_EMAIL': SECONDMENTS_MAIL_LIST[0]}))
            text_template = loader.get_template('crppdmt/email/certified.txt')
            text_content = text_template.render(Context({'expert_request': expert_request,
                                        'NORCAP_FOCAL_POINT': NORCAP_FOCAL_POINTS[expert_request.expert_profile_type.name.strip()],
                                        'SMT_URL': SMT_URL, 'SECONDMENTS_EMAIL': SECONDMENTS_MAIL_LIST[0]}))
            if expert_request.country_representative is not expert_request.supervisor:
                recipients = recipients + [expert_request.country_representative.user.email]
            # add requested agency email address
            if "HEROKU" == deploy_env:
                recipients = recipients + [NORCAP_EMAILS[expert_request.expert_profile_type.name.strip()],]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request, attach_tor=True,
                              attach_letter=True)

        if action == MAIL_REQUEST_NOT_REVIEWED:
            subject = "Expert request rejected for supervisor"
            html_template = loader.get_template('crppdmt/email/rejected_review.html')
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/rejected_review.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.supervisor is not expert_request.request_creator:
                recipients = recipients + [expert_request.request_creator.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)

        if action == MAIL_REQUEST_NOT_CERTIFIED:
            subject = "Expert request rejected for supervisor"
            html_template = loader.get_template('crppdmt/email/rejected_certification.html')
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/rejected_certification.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.country_representative is not expert_request.supervisor:
                recipients = recipients + [expert_request.country_representative.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)

        if action == MAIL_CANDIDATE_APPROVED:
            subject = "Candidate approved for supervisor"
            html_template = loader.get_template('crppdmt/email/candidate_approved.html')
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/rejected_certification.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.country_representative is not expert_request.supervisor:
                recipients = recipients + [expert_request.country_representative.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)



        trace_action(action, expert_request, expert_request.supervisor)

    except:
        print("Error sending email. Request: " + expert_request.name + ", ACTION: " + action)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass



