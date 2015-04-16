# -*- coding: utf-8 -*-
import sys, time, os

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.template.response import TemplateResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.forms.models import modelformset_factory
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response

from crppdmt.settings import BASE_DIR

from crppdmt.models import Person, ExpertRequest, RequestStatus

from crppdmt.forms import  CreateRequest

from crppdmt.constants import *

from crppdmt.shelter_tor import *

from crppdmt.my_ftp import *

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
        #request_list = supervisor_list | creator_list | country_rep_list | field_fp_list | hq_fp_list | expert_list
    except:
        #return redirect('my_login')
        raise Exception(sys.exc_info())


    template = loader.get_template('crppdmt/index.html')
    context = RequestContext(request, {
        'request_list': request_list,
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
def expert_request(request, request_id=None):
    """
    View for the request page
    :param request:
    :param request_id:
    :return:
    """
    query_set = None
    request_form_set = modelformset_factory(ExpertRequest, max_num=1, exclude=[], \
            widgets={'requested_date_of_deployment': forms.TextInput(attrs={'class': 'vDateField'}),
                'desired_date_of_response': forms.TextInput(attrs={'class': 'vDateField'}),
                'date_of_approval_of_candidates': forms.TextInput(attrs={'class': 'vDateField'}),
                'desired_date_of_acceptance_from_agency': forms.TextInput(attrs={'class': 'vDateField'}),
                'date_of_deployment_reported_from_agency': forms.TextInput(attrs={'class': 'vDateField'}),
                'effective_date_of_deployment': forms.TextInput(attrs={'class': 'vDateField'}),
                })
    if request.method == 'POST':
        formset = request_form_set(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect("/index/", context_instance=RequestContext(request))
        else:
            if format(len(formset.errors) > 0):
                num_errors = len(formset.errors[0])
            #set_form_hidden_fields(formset, fields_to_show)
    else:
        query_set = ExpertRequest.objects.filter(pk=request_id)
        formset = request_form_set(queryset=query_set)
        #set_form_hidden_fields(formset, fields_to_show)


    # presentation stuff
    if query_set:
        # to print request name in form caption
        request_name = query_set[0].name
        # to set value for status if not set
        my_request = query_set[0]
        my_request.status = RequestStatus.objects.all()[0]
        my_request.save()
    else:
        request_name = "New Request"
        formset[0].fields['status'].initial=1

    return render_to_response("crppdmt/dmt_request.html",
                              {"formset": formset, "request_name":request_name, \
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
    request_form_set = modelformset_factory(ExpertRequest, max_num=1, form=CreateRequest)

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

            # save expert request instance
            formset.save()

            # upload file to ftp. OBS: after save to avoid problems with document name (duplicates)
            upload_project_file(expert_request.name, str(expert_request.project_document))

            return redirect("/index/", context_instance=RequestContext(request))
        else:
            if format(len(formset.errors) > 0):
                num_errors = len(formset.errors[0])
            #set_form_hidden_fields(formset, fields_to_show)
    else:
        query_set = ExpertRequest.objects.filter(pk=request_id)
        formset = request_form_set(queryset=query_set)

        #set_form_hidden_fields(formset, fields_to_show)

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


def upload_project_file(request_name, document_name):

    # remove document in local file system
    try:
        my_ftp = MyFTP()
        my_ftp.upload_project_file(request_name, document_name)
        os.remove(str(expert_request.project_document))
    except:
        print("Error uploading project file: " + document_name)
        pass # silent remove



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

