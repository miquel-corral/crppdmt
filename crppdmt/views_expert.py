import sys
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


from crppdmt.business_utils import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator
from django.forms.models import modelformset_factory

from crppdmt.models import PersonalDocument, ExpertMessage
from crppdmt.forms import UploadPersonalInfoForm, ExpertMessageForm, DeploymentDateForm
from crppdmt.document_utils import *


@ensure_csrf_cookie
@login_required
def expert_profile(request, expert_id=None):
    """
    View for expert profile page
    :param request:
    :return:
    """
    try:
        user_expert = True
        person = get_person(request)
        # if expert_id person accessing the view is not expert, is supervisor
        if expert_id:
            user_expert = False
            expert = Person.objects.get(id=expert_id)
            if not supervisor_can_access_expert_profile(person, expert):
                return render_to_response("crppdmt/error.html", {"error_description": "Permission denied.",},
                                          context_instance=RequestContext(request))
        else:
            expert = person
        # get personal documents list
        personal_docs = PersonalDocument.objects.filter(expert = expert)
        # get deployment list
        expert_request_list = ExpertRequest.objects.filter(expert=expert)
        # pagination stuff
        paginator = Paginator(expert_request_list, ITEMS_PER_PAGE)  # Limit items per page
        page = request.GET.get('page')
        try:
            requests_paginated = paginator.page(page)
        except:
            print("Unexpected error:", sys.exc_info())
            requests_paginated = paginator.page(1)

        template = loader.get_template('crppdmt/expert/expert_profile.html')
        context = RequestContext(request, {
            'request_list': requests_paginated,
            'username': person.user.username,
            'user': person.user,
            'person': person,
            'personal_docs': personal_docs,
        })
        return HttpResponse(template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def upload_personal_info(request):
    """
    View for the expert upload of personal information
    :param request:
    :param expert_id:
    :return:
    """
    try:
        # get person & control is expert
        person = get_person(request)
        if not person.is_expert():
            return render_to_response("crppdmt/error.html", {"error_description": "Permission denied.",},
                                      context_instance=RequestContext(request))
        # initialization
        request_form_set = modelformset_factory(PersonalDocument, form=UploadPersonalInfoForm, max_num=1, exclude=[])
        query_set = None
        # get personal documents list
        personal_docs = PersonalDocument.objects.filter(expert = person)
        # POST & GET processing
        if request.method == 'POST':
            formset = request_form_set(request.POST, request.FILES)
            # set expert
            if formset.is_valid():
                # get file name and file
                personal_doc = formset[0].save(commit=False)
                # set title if it is not set
                doc_filename = str(personal_doc.file_name)
                if personal_doc.document_title.strip() == '':
                    personal_doc.document_title = str(personal_doc.file_name)[0:len(doc_filename)-4]
                # before ftp
                personal_doc.save()
                # upload doc to ftp
                size = upload_file(person.user.username, str(personal_doc.file_name))
                print("size: " + str(size))
                print("doc_title: " + personal_doc.document_title)
                if size == 0:
                    formset[0].add_error('file_name',"Error uploading file. Try it again later.")
                else:
                    # return to list
                    return redirect("/expert_profile/", context_instance=RequestContext(request))
            else:
                # return to form
                print(formset[0].errors)
                pass
        else:
            # set empty query_set and form
            query_set = PersonalDocument.objects.filter(id=None)
            formset = request_form_set(queryset=query_set)
            # set expert for empty form
            form = formset[0]
            form.fields['expert'].initial = person

        # return
        html_template = loader.get_template('crppdmt/expert/personal_info.html')
        context = RequestContext(request, {"person": person, "formset": formset, 'personal_docs': personal_docs})
        return HttpResponse(html_template.render(context))
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def communicate(request, expert_request_id=None):
    """
    View for the expert to comunicate with supervisor or secondments management team
    :param request:
    :param expert_id:
    :return:
    """
    try:
       # get person & control is expert
        person = get_person(request)
        if not person.is_expert():
            return render_to_response("crppdmt/error.html", {"error_description": "Permission denied.",},
                                      context_instance=RequestContext(request))
        # initialization
        request_form_set = modelformset_factory(ExpertMessage, form=ExpertMessageForm, max_num=1, exclude=[])
        query_set = None
        expert_request = None
        # get personal documents list
        personal_docs = PersonalDocument.objects.filter(expert = person)


        # POST & GET processing
        if request.method == 'POST':
            formset = request_form_set(request.POST, request.FILES)
            # set expert
            if formset.is_valid():
                # get message
                expert_message = formset[0].save(commit=False)
                # check expert_request_id
                if expert_request_id:
                    expert_request = ExpertRequest.objects.get(id=expert_request_id)
                    expert_message.expert_request = expert_request
                # save message
                expert_message.save()
                #send email (will trace)
                send_expert_message_email(expert_message, person, expert_request)
                # return to list
                return redirect("/expert_profile/", context_instance=RequestContext(request))
            else:
                # return to form
                print(formset[0].errors)
                pass
        else:
            # set empty query_set and form
            query_set = ExpertMessage.objects.filter(id=None)
            formset = request_form_set(queryset=query_set)
            # set expert for empty form
            form = formset[0]
            form.fields['expert'].initial = person
            form.fields['expert_request_id'].initial = expert_request_id

        # return
        html_template = loader.get_template('crppdmt/expert/communication.html')
        context = RequestContext(request, {"person": person, "formset": formset, 'personal_docs': personal_docs,})
        return HttpResponse(html_template.render(context))

    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def deployment_date(request, expert_request_id):
    """
    View for the expert to set the deployment date
    :param request:
    :param expert_id:
    :return:
    """
    try:
        # get person from request
        person = get_person(request)
        if not (person.is_supervisor() or person.is_expert()):
            return render_to_response("crppdmt/error.html", {"error_description": "Permission denied.",},
                                      context_instance=RequestContext(request))
        # initialization
        expert_request = None
        form = None

        # POST & GET processing
        if request.method == 'POST':
            form = DeploymentDateForm(data=request.POST)
            if form.is_valid():
                expert_request = ExpertRequest.objects.get(id=expert_request_id)
                expert_request.effective_date_of_deployment = form.cleaned_data['deployment_date']
                expert_request.save()
                trace_action(TRACE_DEPLOYMENT_DATE_SET,expert_request,person)
                if person.is_supervisor():
                    return redirect("/index/", context_instance=RequestContext(request))
                if person.is_expert():
                    return redirect("/expert_profile/", context_instance=RequestContext(request))
            else:
                pass
        else:
            form = DeploymentDateForm()
            form.fields['expert_request_id'].initial = expert_request_id

        # return
        html_template = loader.get_template('crppdmt/expert/deployment_date.html')
        context = RequestContext(request, {"person": person, "form": form, 'is_logout': "logout"})
        return HttpResponse(html_template.render(context))

    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def inception_report(request, expert_id, expert_request_id=None):
    """
    View for the expert to set the inception report
    :param request:
    :param expert_id:
    :return:
    """
    try:
        pass
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))

@ensure_csrf_cookie
@login_required
def per(request, expert_id, expert_request_id=None):
    """
    View for the expert to upload the PER
    :param request:
    :param expert_id:
    :return:
    """
    try:
        pass
    except:
        if debug_is_on():
            raise
        else:
            return render_to_response("crppdmt/error.html",
                                      {"error_description": str(sys.exc_traceback),},
                                      context_instance=RequestContext(request))



