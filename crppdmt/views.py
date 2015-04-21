# -*- coding: utf-8 -*-
import sys
import time
import os
import datetime

from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import modelformset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
from django.core import serializers

from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response

from crppdmt.settings import *

from crppdmt.models import Person, ExpertRequest, GeneralCheckList, TraceAction, RequestStatus

from crppdmt.forms import CreateRequestForm, EditRequestForm, GeneralCheckListForm

from crppdmt.constants import *

from crppdmt.shelter_tor import *

from crppdmt.my_ftp import *
from crppdmt.my_mail import *

@ensure_csrf_cookie
def my_login(request):
    username = ''
    password = ''
    user = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login_response = login(request, user)
                    request.session['username'] = username
                    return redirect('/index/')
                else:
                    # Return a 'disabled account' error message
                    context = {'form': form}
                    return redirect('/login/?next=%s' % request.path)
            else:
                # Return an 'invalid login' error message.
                context = {'form': form}
                return TemplateResponse(request, 'crppdmt/login.html', context)
        else:
            context = {'form': form}
            return TemplateResponse(request, 'crppdmt/login.html', context)
    else:
        form = AuthenticationForm(request)
        context = {'form': form,
                   'is_login': 'is_login',
            }
        return TemplateResponse(request, 'crppdmt/login.html', context)

@ensure_csrf_cookie
def my_logout(request):
    logout(request)
    template = loader.get_template('crppdmt/logout.html')
    context = RequestContext(request, {'is_logout': "logout"})
    return HttpResponse(template.render(context))

@ensure_csrf_cookie
def my_change_password(request):

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            # change password
            #raise Exception("EL USUARIO: " + request.user.username)
            #raise Exception("EL pwd: " + str(request.POST['new_password1']).strip())
            u = User.objects.get(username=request.user.username)
            u.set_password(str(request.POST['new_password1']).strip())
            u.save()
            # logout
            logout(request)
            # return to index page
            return redirect('/index/')
        else:
            context = {'form': form, 'is_login':'is_login'}
            return TemplateResponse(request, 'crppdmt/change_password.html', context)
    else:
        form = PasswordChangeForm(request)
        context = {'form': form,
                   'is_login':'is_login',
            }
        return TemplateResponse(request, 'crppdmt/change_password.html', context)


@ensure_csrf_cookie
@login_required
def index(request):
    """
    View for the list of sections of the index card

    :param request:
    :return:
    """
    request_list = None
    user = None
    person = None
    supervisor_list = None
    creator_list = None
    country_rep_list = None
    field_fp_list = None
    hq_fp_list = None
    expert_list = None

    # get username from session
    username = request.session.get('username')

    if not username:
        return redirect('my_login')
    try:
        person = get_person_by_username(username)
        # get the requests/missions for each role
        request_list = ExpertRequest.objects.filter(expert=None)  ## Dirty to get empty QuerySet

        for role in person.roles.all():  # everyone has at least one role
            if role.name == ROLES["ROLE_SUPERVISOR"]:
                supervisor_list = ExpertRequest.objects.filter(supervisor=person)
                request_list = request_list | supervisor_list
            if role.name == ROLES["ROLE_CREATOR"]:
                creator_list = ExpertRequest.objects.filter(request_creator=person)
                request_list = request_list | creator_list
            if role.name == ROLES["ROLE_COUNTRY_REPRESENTATIVE"]:
                country_rep_list = ExpertRequest.objects.filter(country_representative=person)
                request_list = request_list | country_rep_list
            if role.name == ROLES["ROLE_FIELD_FOCAL_POINT"]:
                field_fp_list = ExpertRequest.objects.filter(field_focal_point=person)
                request_list = request_list | field_fp_list
            if role.name == ROLES["ROLE_HQ_FOCAL_POINT"]:
                hq_fp_list = ExpertRequest.objects.filter(hq_focal_point=person)
                request_list = request_list | hq_fp_list
            if role.name == ROLES["ROLE_EXPERT"]:
                expert_list = ExpertRequest.objects.filter(expert=person)
                request_list = request_list | expert_list

        # concatenate like this only works when querysets from the same model
        if supervisor_list is not None:
            request_list = supervisor_list
        if creator_list is not None:
            request_list = request_list | creator_list
        if country_rep_list is not None:
            request_list = request_list | country_rep_list
        if field_fp_list is not None:
            request_list = request_list | field_fp_list
        if hq_fp_list is not None:
            request_list = request_list | hq_fp_list
        if expert_list is not None:
            request_list = request_list | expert_list
    except:
        #return redirect('my_login')
        raise Exception(sys.exc_info())

    paginator = Paginator(request_list, ITEMS_PER_PAGE)  # Limit items per page
    page = request.GET.get('page')
    try:
        requests_paginated = paginator.page(page)
    except:
        print("Unexpected error:", sys.exc_info())
        requests_paginated = paginator.page(1)

    template = loader.get_template('crppdmt/index.html')
    context = RequestContext(request, {
        'request_list': requests_paginated,
        'username': username,
        'user': user,
        'person': person,
    })
    return HttpResponse(template.render(context))




def my_copyright(request):
    """
    View for the my_copyright page

    :param request:
    :return:
    """
    username = request.session.get('username')
    try:
        index_card = None
        #index_card = IndexCard.objects.get(username=username)
    except:
        index_card = None
    template = loader.get_template('crppdmt/my_copyright.html')
    context = RequestContext(request, {
        'username': username,
        'index_card': index_card,
        'is_copyright': 'is_copyright',
    })
    return HttpResponse(template.render(context))

@ensure_csrf_cookie
@login_required
def edit_request(request, request_id=None):
    """
    View for the request page
    :param request:
    :param request_id:
    :return:
    """
    query_set = None
    # get expert request
    expert_request = ExpertRequest.objects.get(id=request_id)
    # get person
    person = get_person(request)
    # formset
    request_form_set = modelformset_factory(ExpertRequest, form=EditRequestForm, max_num=1, exclude=[], \
            widgets={'requested_date_of_deployment': forms.TextInput(attrs={'class': 'vDateField'}),
                'desired_date_of_response': forms.TextInput(attrs={'class': 'vDateField'}),
                'date_of_approval_of_candidates': forms.TextInput(attrs={'class': 'vDateField'}),
                'desired_date_of_acceptance_from_agency': forms.TextInput(attrs={'class': 'vDateField'}),
                'date_of_deployment_reported_from_agency': forms.TextInput(attrs={'class': 'vDateField'}),
                'effective_date_of_deployment': forms.TextInput(attrs={'class': 'vDateField'}),
                'project_document': forms.FileInput(),
                })

    if request.method == 'POST':
        formset = request_form_set(request.POST, request.FILES)
        if formset.is_valid():
            # get instance
            expert_request = formset[0].save(commit=False)
            # control HQ and field focal point informed
            if not expert_request.agency_hq_focal_point:
                    expert_request.agency_hq_focal_point = expert_request.supervisor
            if not expert_request.agency_field_focal_point:
                    expert_request.agency_field_focal_point = expert_request.supervisor

            if expert_request.project_document:
                # upload file to ftp. OBS: after save to avoid problems with document name (duplicates)
                upload_project_document(expert_request.name, str(expert_request.project_document))

            # save form
            formset.save()
            # trace action
            trace_action("EDIT REQUEST", expert_request, person)
            # check send to supervisor. Tricky validation in python. Check Action!!!
            if formset[0].cleaned_data['send_to_supervisor'] and formset[0].cleaned_data['send_to_supervisor'] is True:
                # redirect to general check list page
                if expert_request.status.name == 'Preparation':
                    return redirect("/general_checklist/to_supervisor/" + str(expert_request.id),
                                    context_instance=RequestContext(request))
                if expert_request.status.name == 'Supervision':
                    return redirect("/general_checklist/to_validation/" + str(expert_request.id),
                                    context_instance=RequestContext(request))
            else:
                # return to request list
                return redirect("/index", context_instance=RequestContext(request))
                """
                # validate no empty fields
                if expert_request.has_no_empty_text_fields():
                    # save expert request instance
                    formset.save()
                    # trace action
                    trace_action("SEND TO SUPERVISOR", expert_request, person)
                    # redirect to general checklist page
                    return redirect("/general_checklist/to_supervision/" + str(expert_request.id), context_instance=RequestContext(request))
                else:
                    formset.errors[0]['Text Fields']='All text fields must be informed .'
            else:
                # Save changes
                formset.save()
                # trace action
                trace_action("EDIT REQUEST", expert_request, person)
                # return to request list
                return redirect("/index", context_instance=RequestContext(request))
                """
        else:
            if format(len(formset.errors) > 0):
                num_errors = len(formset.errors[0])
    else:
        query_set = ExpertRequest.objects.filter(pk=request_id)
        formset = request_form_set(queryset=query_set)


    return render_to_response("crppdmt/edit_request.html",
                              {"formset": formset,
                               "expert_request": expert_request,
                               "BACKGROUND_INFORMATION_HELP_TEXT":BACKGROUND_INFORMATION_HELP_TEXT},
                              context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def create_request(request, request_id=None):
    """
    View for the request page
    :param request:
    :param request_id:
    :return:
    """
    person = get_person(request)
    query_set = None
    request_form_set = modelformset_factory(ExpertRequest, max_num=1, form=CreateRequestForm, exclude=[])
    send_to_supervision = False

    if request.method == 'POST':
        formset = request_form_set(request.POST, request.FILES)

        if formset.is_valid():
            # get instance
            expert_request = formset[0].save(commit=False)
            # control HQ and field focal point informed
            if not expert_request.agency_hq_focal_point:
                    expert_request.agency_hq_focal_point = expert_request.supervisor
            if not expert_request.agency_field_focal_point:
                    expert_request.agency_field_focal_point = expert_request.supervisor
            # set template values
            set_template_values(expert_request)
            # set expert request name
            expert_request.name = expert_request.project_name + "_" + expert_request.expert_profile_type.name + \
                "_" + time.strftime("%Y%m%d%H%M%S")

            # upload file to ftp. OBS: after save to avoid problems with document name (duplicates)
            upload_project_document(expert_request.name, str(expert_request.project_document))

            # save expert request
            formset.save()

            # trace action
            trace_action("CREATE REQUEST", expert_request, person)

            return redirect("/index/", context_instance=RequestContext(request))
        else:
            if format(len(formset.errors) > 0):
                num_errors = len(formset.errors[0])
    else:
        query_set = ExpertRequest.objects.filter(pk=request_id)
        formset = request_form_set(queryset=query_set)


    # initial values
    if not query_set:
        # status: preparation
        formset[0].fields['status'].initial = 1
        # creator
        formset[0].fields['request_creator'].initial = person.id
        # requesting agency
        formset[0].fields['requesting_agency'].initial = "UN-HABITAT"
        # name. temporary value to not duplicate an so validate model form
        formset[0].fields['name'].initial = time.strftime("%Y%m%d%H%M%S")

    return render_to_response("crppdmt/create_request.html",
                              {"formset": formset, "person": person,
                               "IF_OTHER_THAN_SUPERVISOR_HELP_TEXT": IF_OTHER_THAN_SUPERVISOR_HELP_TEXT },
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def general_checklist(request, action, expert_request_id):
    """
    View to present general checklist page
    :param request:
    :param action:
    :param expert_request_id:
    :return:
    """

    print("general_checklist. action: " + action);

    # get expert request
    expert_request = ExpertRequest.objects.get(id=expert_request_id)

    # get person
    person = get_person(request)

    # access control
    if expert_request.status.name == "Supervision" and \
            (expert_request.supervisor == person or expert_request.request_creator == person):
        pass
    else:
        pass  #TODO: redirect to control access page


    # get check list
    all_items = GeneralCheckList.objects.all().order_by('id')
    # error required ack
    error_required_ack = False
    if request.method == 'POST':
        my_form = GeneralCheckListForm(request.POST)

        if my_form.is_valid():
            # get request
            expert_request = ExpertRequest.objects.get(id=expert_request_id)
            # get value of action
            print("action: " + action)

            # settings per action
            if action == "to_supervisor":
                expert_request.date_sent_to_supervisor = datetime.datetime.date(datetime.datetime.now())
                expert_request.status = RequestStatus.objects.get(name="Supervision")
                # update expert request
                expert_request.save()
                # send email to supervisor
                send_request_email_to(expert_request, "Supervisor")
                # trace action
                trace_action("REQUEST TO SUPERVISOR", expert_request, person)

            if action == "to_validation":
                expert_request.date_sent_to_validation = datetime.datetime.date(datetime.datetime.now())
                expert_request.status = RequestStatus.objects.get(name="Validation")
                # update expert request
                expert_request.save()
                # send email to validator
                send_request_email_to(expert_request, "Validator")
                # trace action
                trace_action("REQUEST TO VALIDATOR", expert_request, person)


            # back to request list page
            return redirect("/index/", context_instance=RequestContext(request))
        else:
            error_required_ack = True
    else:
        # empty form
        my_form = GeneralCheckListForm()


    paginator = Paginator(all_items, ITEMS_PER_PAGE)  # Limit items per page
    page = request.GET.get('page')
    try:
        item_list = paginator.page(page)
    except:
        print("Unexpected error:", sys.exc_info())
        item_list = paginator.page(1)

    return render_to_response("crppdmt/general_checklist.html",
                              {"item_list": item_list,
                               "person": person,
                               "form": my_form,
                               "action": action,
                               "expert_request_id": expert_request_id,
                               "expert_request_name": expert_request.name,
                               "error_required_ack":error_required_ack},
                              context_instance=RequestContext(request))





def test(request):
    """
    View for testing purposes
    :param request:
    :return:
    """
    return render_to_response("crppdmt/test.html",
                              context_instance=RequestContext(request))


def generate_letter_of_request_pdf(request, expert_request_id):
    """
    Generates letter of request PDF request
    :param request:
    :param expert_request_id:
    :return:
    """
    expert_request = ExpertRequest.objects.get(pk=expert_request_id)
    context = {'expert_request': expert_request,
               'pagesize': 'A4',
               'BASE_DIR': BASE_DIR,
            }

    return render_to_pdf_response(request, "crppdmt/letter_of_request.html", context, filename=None, encoding=u'utf-8')


def generate_tor_pdf(request, expert_request_id):
    """
    Generates ToR PDF request
    :param request:
    :param expert_request_id:
    :return:
    """
    expert_request = ExpertRequest.objects.get(pk=expert_request_id)
    context = {'expert_request': expert_request,
               'pagesize': 'A4',
               'BASE_DIR': BASE_DIR,
            }

    return render_to_pdf_response(request, "crppdmt/tor.html", context, filename=None, encoding=u'utf-8')


def retrieve_file(request, remote_folder, remote_file):
    """
    retrieve_file
    :param request:
    :param expert_request_id:
    :return:
    """

    # get the file
    file_content = get_ftp_file_content(remote_folder, remote_file)
    if file_content is None:
        print("file_content is null!!")  # TODO: redirect to error page
    else:
        # return the file
        response = HttpResponse(file_content, content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=' + remote_file
        return response




############################################################
#
# Class views
#
#############################################################


class GenerateToRPDF(PDFTemplateView):
    """
    Generates PDF for ToR
    """
    template_name = "crppdmt/tor.html"
    expert_request = ExpertRequest

    def get_context_data(self, **kwargs):
        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="ToR",
            **kwargs
        )


class HelloPDFView(PDFTemplateView):
    template_name = "crppdmt/test_pdf.html"

    def get_context_data(self, **kwargs):
        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Hi there!",
            **kwargs
        )


############################################################
#
# Utilities functions
#
#############################################################

# Helper functions
def get_person(request):
    """
    Get person from request
    :param request:
    :return:
    """
    # get username
    username = request.session.get('username')
    return get_person_by_username(username)


def get_user_by_username(username):
    """
    Get person by username
    :param username:
    :return:
    """
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    return user


############################################################
#
# Expert Request functions
#
#############################################################
def set_template_values(expert_request):
    """
    sets template values as a function of expert type
    :param expert_request:
    :return:
    """
    if expert_request.expert_profile_type.name == PROFILE_SHELTER:
        expert_request.objectives_and_scope = SHELTER_OBJECTIVES
        expert_request.expert_profile = SHELTER_EXPERT_PROFILE
        expert_request.expected_outputs = SHELTER_EXPECTED_OUTPUTS
        expert_request.main_duties_and_responsibilities = SHELTER_KEY_DUTIES
        expert_request.other_relevant_information = SHELTER_OTHER_RELEVANT_INFO


def get_person_by_username(username):
    """
    Get person by username
    :param username:
    :return:
    """
    user = get_user_by_username(username)
    if user:
        try:
            person = Person.objects.get(user=user)
        except:
            person = None
        return person
    else:
        return None


def upload_project_document(request_name, document_name):

    # remove document in local file system
    try:
        my_ftp = MyFTP()
        my_ftp.upload_file(document_name, request_name, document_name)
        os.remove(document_name)
    except:
        print("Error uploading project file: " + document_name)
        pass  # silent remove


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


def send_request_email_to(expert_request, action):
    try:
        my_mail = MyMail()
        subject = "DMT - New Expert Request to Validate"
        html_template = loader.get_template('crppdmt/email/supervisor.html')
        html_content = html_template.render(Context({'request_name': expert_request.name,}))
        text_template = loader.get_template('crppdmt/email/supervisor.txt')
        text_content = text_template.render(Context({'request_name': expert_request.name,}))
        recipients = [expert_request.supervisor.user.email]
        if action == "Supervision":
            if expert_request.supervisor is not expert_request.request_creator:
                recipients = recipients + [expert_request.request_creator.user.email]
        if action == "Validation":
            recipients = recipients + [expert_request.country_representative.user.email]
        # send email
        my_mail.send_mail(subject, html_content, text_content, recipients)
    except:
        print("Error sending email to supervisor. Request: " + expert_request.name)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass


def trace_action(action_name, expert_request, person):
    try:
        print("Expert requ.name: " + expert_request.name)
        new_log = TraceAction()
        new_log.action = action_name
        new_log.expert_request = expert_request
        print("new_log.expert_request: " + new_log.expert_request.name)
        new_log.description = serializers.serialize('xml', [expert_request])
        print("Expert requ.name: " + expert_request.name)
        new_log.person = person
        new_log.save()
    except:
        print("Error tracing object: " + expert_request.name)
        print("Error: " + str(sys.exc_info()))



# Form utilities
def set_form_hidden_fields(formset, fields_to_show):
    """
    Function to set hidden fields and show fields of each form in formset
    :param formset:
    :param files_to_show:
    :return:
    """
    for form in formset:
        for field in form.fields:
            if not any(field in s for s in fields_to_show):
                form.fields[field].widget = forms.HiddenInput()


def set_form_hidden_fields_hidden_fields(formset, fields_to_hide):
    """
    Function to set hidden fields and show fields of each form in formset
    :param formset:
    :param files_to_show:
    :return:
    """
    for form in formset:
        for field in form.fields:
            if field in fields_to_hide:
                form.fields[field].widget = forms.HiddenInput()


def set_form_readonly_fields(formset, read_only_fields):
    """
    Function to set readonly fields of each form in formset
    :param formset:
    :return:
    """
    for form in formset:
        for field in form.fields:
            print(field)
            if any(field in s for s in read_only_fields):
                print(field)
                form.fields[field].widget.attrs['disabled'] = True


def set_form_country_select(formset):
    for form in formset:
        for field in form.fields:
            print(field)
            fields_to_change = ('country')
            if any (field in s for s in fields_to_change):
                #form.fields[field] = forms.MultipleChoiceField(choices=CHOICES_YES_NO, blank=True)
                # This works to change choices: form.fields[field].widget.attrs['choices'] = CHOICES_YES_NO
                form.fields[field].widget = forms.Select(choices=CHOICES_YES_NO)

