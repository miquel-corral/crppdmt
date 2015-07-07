import time

from django import forms
from django.contrib.auth.models import User
from constants import *
from crppdmt.models import ExpertRequest, Person, Role, Organization
from captcha.fields import CaptchaField

class BasicRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BasicRequestForm, self).__init__(*args, **kwargs)

        # Date widget for requested date of deployment
        self.fields['requested_date_of_deployment'].widget = forms.TextInput(attrs={'class': 'vDateField'})

        # ClearableFileInput widget for upload file field
        self.fields['project_document'].widget = forms.FileInput()

        # filter people with role supervisor
        self.fields['supervisor'].queryset = Person.objects.filter(roles__name=ROLES[ROLE_SUPERVISOR_ITEM])
        # filter people with role country representative
        self.fields['country_representative'].queryset = Person.objects.filter(roles__name=
                                                                               ROLES[ROLE_COUNTRY_REPRESENTATIVE_ITEM])
        # filter people with role HQ focal point
        self.fields['agency_hq_focal_point'].queryset = Person.objects.filter(roles__name=
                                                                              ROLES[ROLE_HQ_FOCAL_POINT_ITEM])
        # filter people with role Field focal point
        self.fields['agency_field_focal_point'].queryset = Person.objects.filter(roles__name=
                                                                                 ROLES[ROLE_FIELD_FOCAL_POINT_ITEM])
        # filter requested agencies: organizations with requested agency type
        self.fields['requested_agency'].queryset = Organization.objects.filter(type=ORGANIZATION_TYPE_REQUESTED)

    class Meta:
        model = ExpertRequest
        # exclude fields
        exclude = ['background_information', 'objectives_and_scope', 'expert_profile', 'expected_outputs',
                   'main_duties_and_responsibilities', 'other_relevant_information', 'date_of_request_sent',
                   'date_of_approval_of_candidates', 'desired_date_of_acceptance_from_agency',
                   'date_of_deployment_reported_from_agency', 'effective_date_of_deployment',
                   'date_of_closure_of_request', 'date_sent_to_supervisor', 'date_sent_to_validation']


class CreateRequestForm(BasicRequestForm):
    #send_to_supervisor = forms.BooleanField(required=False, initial=False)  # initial force always return boolean field
    pass


class EditRequestForm(BasicRequestForm):
    send_to_supervisor = forms.BooleanField(required=False, initial=False)  # initial force always return boolean field


class GeneralCheckListForm(forms.Form):
    # initial force always return boolean field
    check_field = forms.BooleanField(required=True, initial=False, label="I have read the above commitments")


class SummaryCheckListForm(forms.Form):
    # initial force always return boolean field
    validate_request = forms.BooleanField(required=True, initial=False, label="Acknowledgment of the above commitments")


class RejectRequestForm(BasicRequestForm):

    def __init__(self, *args, **kwargs):
        super(BasicRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ExpertRequest
        exclude = []


class UserRegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # set widget for roles as multiplehiddeninput
        self.fields['roles'].widget = forms.MultipleHiddenInput()
        # possible supervisors to certify registration
        user_ids = Person.objects.filter(roles__name=ROLES[ROLE_COUNTRY_REPRESENTATIVE_ITEM]).values_list('user_id',
                                                                                                          flat=True)
        users = User.objects.filter(id=-1)
        for user_id in user_ids:
            users = users | User.objects.filter(id=user_id)
        self.fields['certifier'].queryset = users


    captcha = CaptchaField()

    class Meta:
        model = Person
        exclude = []


class UserValidationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserValidationForm, self).__init__(*args, **kwargs)
        self.fields['rejection_reason'].widget = forms.Textarea()

    supervisor_role = forms.BooleanField(required=False)
    rejection_reason = forms.CharField(required=False)
    rejected = forms.BooleanField(required=False)

    class Meta:
        model = Person
        exclude = []







