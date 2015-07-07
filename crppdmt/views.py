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
from easy_pdf.rendering import render_to_pdf_response, render_to_pdf

from crppdmt.settings import *

from crppdmt.models import Person, ExpertRequest, GeneralCheckList, TraceAction, RequestStatus, Organization, Role

from crppdmt.forms import CreateRequestForm, EditRequestForm, GeneralCheckListForm, SummaryCheckListForm, \
    RejectRequestForm, UserRegistrationForm, UserValidationForm

from crppdmt.constants import *

from crppdmt.shelter_tor import *

from crppdmt.my_ftp import *
from crppdmt.my_mail import *

import crppdmt.summary_checklist

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
    try:
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
    except:
        if DEBUG:
            raise
        else:
            return redirect("/index/", context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def index(request):
    """
    View for the list of sections of the index card

    :param request:
    :return:
    """
    try:
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
        person = get_person_by_username(username)

        if not username or not person:
            return redirect('my_login')
        try:

            # get the requests/missions for each role
            request_list = ExpertRequest.objects.filter(expert=None)  # Dirty to get empty QuerySet

            for role in person.roles.all():  # everyone has at least one role
                if role.name == ROLES[ROLE_SUPERVISOR_ITEM]:
                    supervisor_list = ExpertRequest.objects.filter(supervisor=person)
                if role.name == ROLES[ROLE_CREATOR_ITEM]:
                    creator_list = ExpertRequest.objects.filter(request_creator=person)
                if role.name == ROLES[ROLE_COUNTRY_REPRESENTATIVE_ITEM]:
                    country_rep_list = ExpertRequest.objects.filter(country_representative=person)
                if role.name == ROLES[ROLE_FIELD_FOCAL_POINT_ITEM]:
                    field_fp_list = ExpertRequest.objects.filter(agency_field_focal_point=person)
                if role.name == ROLES[ROLE_HQ_FOCAL_POINT_ITEM]:
                    hq_fp_list = ExpertRequest.objects.filter(agency_hq_focal_point=person)
                if role.name == ROLES[ROLE_EXPERT_ITEM]:
                    expert_list = ExpertRequest.objects.filter(expert=person)

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
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))


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
    template = loader.get_template('crppdmt/copyright.html')
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
    try:
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
                    # upload file to ftp. OBS: check existence of project doc. file to avoid errors if doc.
                    # has not changed while modifying the request
                    if os.path.isfile(str(expert_request.project_document)):
                        upload_project_document(expert_request.name, str(expert_request.project_document))
                    else:
                        pass  # file not modified while editing the request
                # save form
                formset.save()
                # trace action
                trace_action(TRACE_EDIT_REQUEST, expert_request, person)
                # check send to supervisor. Tricky validation in python. Check Action!!!
                if formset[0].cleaned_data['send_to_supervisor'] and formset[0].cleaned_data['send_to_supervisor'] is True:
                    # redirect to general check list page
                    if expert_request.status.name == STATUS_PREPARATION:
                        return redirect("/general_checklist/to_supervisor/" + str(expert_request.id),
                                        context_instance=RequestContext(request))
                    if expert_request.status.name == STATUS_SUPERVISION:
                        if expert_request.has_empty_text_fields() or expert_request.has_no_changed_text_fields():
                            formset.errors[0][ToR_FIELDS] = ToR_FIELDS_VALIDATION_ERROR
                        else:
                            # ensure supervisor looks at checklist only if he was not the creator
                            if expert_request.supervisor != expert_request.request_creator:
                                return redirect("/general_checklist/to_certification/" + str(expert_request.id),
                                        context_instance=RequestContext(request))
                            # if not request goes directly to validation
                            else:
                                # change status
                                expert_request.status = RequestStatus.objects.get(name=STATUS_CERTIFICATION)
                                expert_request.save()
                                # trace
                                trace_action(TRACE_REQUEST_TO_CERTIFICATION, expert_request, person)
                                # send email to validator
                                send_request_email_to(expert_request, MAIL_REQUEST_TO_CERTIFY)
                                return redirect("/index", context_instance=RequestContext(request))
                else:
                    # return to request list
                    return redirect("/index", context_instance=RequestContext(request))
            else:
                if format(len(formset.errors) > 0):
                    num_errors = len(formset.errors[0])
        else:
            query_set = ExpertRequest.objects.filter(pk=request_id)
            formset = request_form_set(queryset=query_set)

        return render_to_response("crppdmt/edit_request.html",
                                  {"formset": formset,
                                   "expert_request": expert_request,
                                   "BACKGROUND_INFORMATION_HELP_TEXT": BACKGROUND_INFORMATION_HELP_TEXT,
                                   "ToR_FIELDS": ToR_FIELDS,
                                   "IF_OTHER_THAN_SUPERVISOR_HELP_TEXT": IF_OTHER_THAN_SUPERVISOR_HELP_TEXT,
                                   "SMT_URL": SMT_URL},
                                  context_instance=RequestContext(request))
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
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
    try:
        person = get_person(request)
        query_set = None
        request_form_set = modelformset_factory(ExpertRequest, max_num=1, form=CreateRequestForm, exclude=[])

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
                trace_action(TRACE_CREATE_REQUEST, expert_request, person)

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
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
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
    try:
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
                # settings per action
                if action == ACTION_TO_SUPERVISOR:
                    expert_request.date_sent_to_supervisor = datetime.datetime.date(datetime.datetime.now())
                    expert_request.status = RequestStatus.objects.get(name="Supervision")
                    # update expert request
                    expert_request.save()
                    # send email to supervisor
                    send_request_email_to(expert_request, MAIL_REQUEST_TO_REVIEW)
                    # trace action
                    trace_action(TRACE_REQUEST_TO_SUPERVISOR, expert_request, person)

                if action == ACTION_TO_CERTIFICATION:
                    expert_request.date_sent_to_validation = datetime.datetime.date(datetime.datetime.now())
                    expert_request.status = RequestStatus.objects.get(name=STATUS_CERTIFICATION)
                    # update expert request
                    expert_request.save()
                    # send email to validator
                    send_request_email_to(expert_request, MAIL_REQUEST_TO_CERTIFY)
                    # trace action
                    trace_action(TRACE_REQUEST_TO_CERTIFICATION, expert_request, person)


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
                                   "ACTION_TO_SUPERVISOR": ACTION_TO_SUPERVISOR,
                                   "ACTION_TO_CERTIFICATION": ACTION_TO_CERTIFICATION,
                                   "expert_request_id": expert_request_id,
                                   "expert_request_name": expert_request.name,
                                   "error_required_ack":error_required_ack},
                                  context_instance=RequestContext(request))
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def summary_checklist(request, expert_request_id):
    """
    View to validate a request (and send to partner organization)
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        # get expert request
        expert_request = ExpertRequest.objects.get(id=expert_request_id)
        # get person
        person = get_person(request)

        if request.method == 'POST':
            my_form = SummaryCheckListForm(request.POST)

            if my_form.is_valid():
                # actions if validated
                if my_form.cleaned_data['validate_request'] and my_form.cleaned_data['validate_request'] is True:
                    # change status
                    expert_request.status = RequestStatus.objects.get(name=STATUS_CANDIDATE_APPROVAL)
                    # save request
                    expert_request.save()
                    # trace
                    trace_action(TRACE_VALIDATED_REQUEST,expert_request, person)
                    # send email to validator and supervisor
                    send_request_email_to(expert_request, MAIL_REQUEST_CERTIFIED)
                    # trace
                    trace_action(TRACE_VALIDATED_REQUEST_TO_SUPERVISOR,expert_request, person)
                    # send email to NORCAP
                    send_request_email_to(expert_request, MAIL_REQUEST_CERTIFIED)
                    # trace
                    trace_action(TRACE_VALIDATED_REQUEST_TO_NORCAP,expert_request, person)

                # back to request list page
                return redirect("/index/", context_instance=RequestContext(request))
            else:
                pass
        else:
            # empty form
            my_form = SummaryCheckListForm()

        return render_to_response("crppdmt/summary_checklist.html",
                                  {"person": person,
                                   "form": my_form,
                                   "expert_request_id": expert_request_id,
                                   "expert_request_name": expert_request.name ,
                                   "summary_literals": crppdmt.summary_checklist ,},
                                   context_instance=RequestContext(request))
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def copy_request(request, expert_request_id):
    """
    View to copy a request to further edit it
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        # get person
        person = get_person(request)
        # copy request
        expert_request = ExpertRequest.objects.get(id=expert_request_id)
        expert_request.pk = None
        expert_request.status = RequestStatus.objects.get(name=STATUS_PREPARATION)
        expert_request.name = expert_request.project_name + "_" + expert_request.expert_profile_type.name + \
                    "_" + time.strftime("%Y%m%d%H%M%S")
        expert_request.save()
        # trace action
        trace_action(TRACE_COPIED_REQUEST,expert_request, person)
        # return to index
        return redirect('/index/')
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def extend_request(request, expert_request_id):
    """
    View to extend a request to further edit it
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        # get person
        person = get_person(request)
        # extend request
        expert_request = ExpertRequest.objects.get(id=expert_request_id)
        expert_request.pk = None
        expert_request.status = RequestStatus.objects.get(name=STATUS_PREPARATION)
        expert_request.name = expert_request.project_name + "_" + expert_request.expert_profile_type.name + \
                    "_" + time.strftime("%Y%m%d%H%M%S")
        expert_request.first_request = "NO"
        expert_request.extension = ""
        expert_request.save()
        # trace action
        trace_action(TRACE_EXTENDED_REQUEST,expert_request, person)
        # return to index
        return redirect('/index/')
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def reject_request(request, expert_request_id):
    """
    View to reject a request (either in review or certify status)
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        # get the request
        expert_request = ExpertRequest.objects.get(id=expert_request_id)
        # get person
        person = get_person(request)

        print("Person: " + person.name)

        #
        query_set = None
        request_form_set = modelformset_factory(ExpertRequest, form=RejectRequestForm, max_num=1, exclude=[], \
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

            print("BEFORE IS VALID")

            if formset.is_valid():
                # get instance
                expert_request = formset[0].save(commit=False)

                print("expert_request: " + expert_request.name)

                # actions according status
                if expert_request.status.name == STATUS_SUPERVISION:
                    # control of reject reason
                    if expert_request.rejected_review_reason.strip() == '':
                        formset.errors[0]['rejected_review_reason'] = REJECT_REASON_VALIDATION_ERROR
                        return render_to_response("crppdmt/reject_request.html",
                                                  {"person": person,
                                                   "expert_request": expert_request,
                                                   "formset": formset,},
                                                  context_instance=RequestContext(request))
                    else:
                        # reject actions
                        expert_request.reject_review_date = time.strftime("%Y%m%d%H%M%S")
                        expert_request.status = RequestStatus.objects.get(name=STATUS_PREPARATION)
                        trace_action(TRACE_REJECTED_REVIEW_REQUEST, expert_request, person)
                        send_request_email_to(expert_request, MAIL_REQUEST_NOT_REVIEWED)

                if expert_request.status.name == STATUS_CERTIFICATION:
                    # control of reject reason
                    if expert_request.rejected_certification_reason.strip() == '':
                        formset.errors[0]['rejected_certification_reason'] = REJECT_REASON_VALIDATION_ERROR
                        return render_to_response("crppdmt/reject_request.html",
                                                  {"person": person,
                                                   "expert_request": expert_request,
                                                   "formset": formset,},
                                                  context_instance=RequestContext(request))

                    else:
                        # reject actions
                        expert_request.reject_certification_date = time.strftime("%Y%m%d%H%M%S")
                        expert_request.status = RequestStatus.objects.get(name=STATUS_SUPERVISION)
                        trace_action(TRACE_REJECTED_CERTIFICATION_REQUEST, expert_request, person)
                        send_request_email_to(expert_request, MAIL_REQUEST_NOT_CERTIFIED)

                # save expert request
                formset.save()

                return redirect("/index/", context_instance=RequestContext(request))
            else:

                for error in formset.errors:
                    print("ERROR: " + str(error))

                if format(len(formset.errors) > 0):
                    num_errors = len(formset.errors[0])
        else:
            query_set = ExpertRequest.objects.filter(pk=expert_request_id)
            formset = request_form_set(queryset=query_set)

            return render_to_response("crppdmt/reject_request.html",
                                      {"person": person,
                                       "expert_request": expert_request,
                                       "formset": formset,
                                       "SMT_URL": SMT_URL},
                                      context_instance=RequestContext(request))

    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                  {"error_description": sys.exc_info(),},
                                  context_instance=RequestContext(request))

@ensure_csrf_cookie
def user_registration(request):
    """
    View for new user registration
    :param request:
    :return:
    """
    try:
        query_set = None
        request_form_set = modelformset_factory(Person, max_num=1, form=UserRegistrationForm, exclude=[])

        if request.method == 'POST':
            formset = request_form_set(request.POST, request.FILES)

            if formset.is_valid():
                # get person data
                person = formset[0].save(commit=False)
                # check existence of user with same first and last names
                user_exists = User.objects.filter(first_name=person.first_name, last_name=person.last_name)
                if user_exists:
                    formset[0].add_error('first_name',"User with same first and last name already registered.")
                else:
                    # set person additional information
                    person.name = person.last_name + ", " + person.first_name
                    # create user deactivated, person after and then set role creator
                    user = User()
                    user.username = (person.first_name + "." + person.last_name).replace(" ", "")
                    user.first_name = person.first_name
                    user.last_name = person.last_name
                    user.email = person.email
                    user.is_active = False
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    person.user = user
                    person.save()
                    person.roles.add(Role.objects.get(name=ROLES[ROLE_CREATOR_ITEM]))
                    person.save()
                    # trace
                    trace_action(TRACE_USER_REGISTERED, None,person)
                    # send email
                    send_user_registration_email(person, person.certifier)
                    # redirect to informative page
                    return render_to_response("crppdmt/user_registered.html",{"is_logout":'logout'},context_instance=RequestContext(request))
            else:
                if format(len(formset.errors) > 0):
                    num_errors = len(formset.errors[0])
        else:
            query_set = Person.objects.filter(first_name='')
            formset = request_form_set(queryset=query_set)
            # default values
            if not query_set:
                formset[0].fields['organization'].initial = Organization.objects.get(name='UN-HABITAT').id # UN-HABITAT id
                formset[0].fields['name'].initial = ' '  # just blank name for now, will change in POST treatement
                # roles initial is a list because of ManyToMany Field. Initial = Creator
                formset[0].fields['roles'].initial = [Role.objects.get(name=ROLES[ROLE_CREATOR_ITEM])]
                formset[0].fields['user'].initial = 1  # will change in POST treatement

        return render_to_response("crppdmt/user_registration.html",
                                  {"formset": formset, "SECONDMENTS_EMAIL": SECONDMENTS_MAIL_LIST[0]},
                                  context_instance=RequestContext(request))

    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
def user_registered(request):
    logout(request)
    template = loader.get_template('crppdmt/logout.html')
    context = RequestContext(request, {'is_logout': "logout"})
    return HttpResponse(template.render(context))

@ensure_csrf_cookie
@login_required
def inactive_users(request):
    """
    View for inactive users list
    :param request:
    :return:
    """
    try:
        # get person from session
        person = get_person(request)
        if not person:
            return redirect('my_login')

        # get the inactive users for the person logged
        first_list = Person.objects.filter(certifier=person.user)
        inactive_users_list = [person for person in first_list if person.user.is_active is False]

        # pagination
        paginator = Paginator(inactive_users_list, ITEMS_PER_PAGE)  # Limit items per page
        page = request.GET.get('page')
        try:
            users_paginated = paginator.page(page)
        except:
            print("Unexpected error:", sys.exc_info())
            users_paginated = paginator.page(1)

        template = loader.get_template('crppdmt/inactive_users.html')
        context = RequestContext(request, {
            'users_list': users_paginated,
            'person': person,
        })
        return HttpResponse(template.render(context))

    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def validate_user(request, person_id):
    """
    View to validate / reject user registration
    :param request:
    :return:
    """
    try:
        query_set = None
        form_set = modelformset_factory(Person, max_num=1, form=UserValidationForm, exclude=[])
        # get person to validate / reject
        person = Person.objects.get(id=person_id)

        if request.method == 'POST':
            formset = form_set(request.POST, request.FILES)
            if formset.is_valid():
                # get person data
                person = formset[0].save(commit=False)
                # get action validated or rejected
                if formset[0].cleaned_data['rejected'] and formset[0].cleaned_data['rejected'] is True:
                    # check rejected reason
                    if not formset[0].cleaned_data['rejection_reason'] or str(formset[0].cleaned_data['rejection_reason']).strip() == '':
                            formset.errors[0]['rejection_reason'] = REJECT_REASON_VALIDATION_ERROR

                            return render_to_response("crppdmt/validate_user.html",
                                                      {"person": person,
                                                       "formset": formset,},
                                                      context_instance=RequestContext(request))
                    else:
                        rejection_reason = formset[0].cleaned_data['rejection_reason']
                        # if rejected ok trace and send email.
                        trace_action(TRACE_USER_REJECTED, None, person)
                        #send mail
                        send_user_validation_email(person, rejection_reason)
                        # redirect to inactive users list
                        return redirect("/inactive_users/",context_instance=RequestContext(request))

                else:
                    # check if supervisor
                    if formset[0].cleaned_data['rejected'] and formset[0].cleaned_data['rejected'] is True:
                        person.roles.add(Role.objects.get(name=ROLES[ROLE_SUPERVISOR_ITEM]))
                    # activate user
                    person.user.is_active = True
                    # save user and person
                    person.user.save()
                    person.save()
                    # trace
                    trace_action(TRACE_USER_VALIDATED, None, person)
                    # send email
                    send_user_validation_email(person)
                    # redirect to inactive users list
                    return redirect("/inactive_users/",context_instance=RequestContext(request))
            else:
                if format(len(formset.errors) > 0):
                    num_errors = len(formset.errors[0])

        else:
            query_set = Person.objects.filter(pk=person_id)
            formset = form_set(queryset=query_set)

            return render_to_response("crppdmt/validate_user.html",
                                      {"person": person,
                                       "formset": formset,},
                                      context_instance=RequestContext(request))
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))


def test(request):
    """
    View for testing purposes
    :param request:
    :return:
    """
    return render_to_response("crppdmt/test.html",
                              context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def generate_letter_of_request_pdf(request, expert_request_id):
    """
    Generates letter of request PDF request
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        expert_request = ExpertRequest.objects.get(pk=expert_request_id)
        test = False
        deploy_env = os.environ.get('DEPLOY_ENV','LOCAL')
        if "HEROKU" != deploy_env:
            test = True

        context = {'expert_request': expert_request,
                   'pagesize': 'A4',
                   'BASE_DIR': os.path.join(BASE_DIR, 'crppdmt/static/'),
                   'test_env': test,
                }
        return render_to_pdf_response(request, "crppdmt/pdf/letter_of_request.html", context, filename=None, encoding=u'utf-8')
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def generate_tor_pdf(request, expert_request_id):
    """
    Generates ToR PDF request
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        expert_request = ExpertRequest.objects.get(pk=expert_request_id)
        test = False
        deploy_env = os.environ.get('DEPLOY_ENV','LOCAL')
        if "HEROKU" != deploy_env:
            test = True

        context = {'expert_request': expert_request,
                   'pagesize': 'A4',
                   'BASE_DIR': os.path.join(BASE_DIR, './static/crppdmt/'),
                   'test_env': test,
                }
        return render_to_pdf_response(request, "crppdmt/pdf/tor.html", context, filename=None, encoding=u'utf-8')
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info() + '\n' + sys.exc_traceback,},
                                      context_instance=RequestContext(request))


@ensure_csrf_cookie
@login_required
def retrieve_file(request, remote_folder, remote_file):
    """
    retrieve_file
    :param request:
    :param expert_request_id:
    :return:
    """
    try:
        # get the file
        file_content = get_ftp_file_content(remote_folder, remote_file)
        if file_content is None:
            raise Exception("file_content is null!!")
        else:
            # return the file
            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = 'inline;filename=' + remote_file
            return response
    except:
        if DEBUG:
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": sys.exc_info(),},
                                      context_instance=RequestContext(request))



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
        expert_request.background_information = SHELTER_BACKGROUND_INFO


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

        print("FTP. document_name: " + document_name)

        my_ftp = MyFTP()
        my_ftp.upload_file(document_name, request_name, document_name)
        os.remove(document_name)
    except:
        print("Error uploading project file: " + document_name)
        print(sys.exc_info())
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
            html_content = html_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            text_template = loader.get_template('crppdmt/email/certified.txt')
            text_content = text_template.render(Context({'expert_request': expert_request, 'SMT_URL': SMT_URL}))
            if expert_request.country_representative is not expert_request.supervisor:
                recipients = recipients + [expert_request.country_representative.user.email]
            # send email
            my_mail.send_mail(subject, html_content, text_content, recipients, expert_request)
            # add requested agency email address
            if "HEROKU" == deploy_env:
                recipients = recipients + NORCAP_EMAILS[expert_request.expert_profile_type]
                for recipient in recipients:
                    print("Recipient: " + str(recipient))
            else:
                # TODO: review
                recipients = recipients + [EMAIL_ADDRESS_NORCAP]

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

        trace_action(action, expert_request, expert_request.supervisor)

    except:
        print("Error sending email. Request: " + expert_request.name + ", ACTION: " + action)
        print("Error: " + str(sys.exc_info()))
        pass  # silent remove
    finally:
        pass


def trace_action(action_name, expert_request, person):
    try:
        new_log = TraceAction()
        new_log.action = action_name
        new_log.expert_request = expert_request
        if expert_request:
            new_log.description = serializers.serialize('xml', [expert_request])
        new_log.person = person
        new_log.save()
    except:
        print("Error tracing action: " + action_name)
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

