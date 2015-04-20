import time

from django import forms
from constants import *
from crppdmt.models import ExpertRequest, Person, Role

class BasicRequest(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BasicRequest, self).__init__(*args, **kwargs)

        # Date widget for requested date of deployment
        self.fields['requested_date_of_deployment'].widget = forms.TextInput(attrs={'class': 'vDateField'})

        # ClearableFileInput widget for upload file field
        self.fields['project_document'].widget = forms.ClearableFileInput()

        # filter people with role supervisor
        self.fields['supervisor'].queryset = Person.objects.filter(roles__name=ROLES["ROLE_SUPERVISOR"])
        # filter people with role country representative
        self.fields['country_representative'].queryset = Person.objects.filter(roles__name=
                                                                               ROLES["ROLE_COUNTRY_REPRESENTATIVE"])
        # filter people with role HQ focal point
        self.fields['agency_hq_focal_point'].queryset = Person.objects.filter(roles__name=
                                                                              ROLES["ROLE_HQ_FOCAL_POINT"])
        # filter people with role Field focal point
        self.fields['agency_field_focal_point'].queryset = Person.objects.filter(roles__name=
                                                                                 ROLES["ROLE_FIELD_FOCAL_POINT"])

    class Meta:
        model = ExpertRequest
        # exclude fields
        exclude = ['background_information', 'objectives_and_scope', 'expert_profile', 'expected_outputs',
                   'main_duties_and_responsibilities', 'other_relevant_information', 'date_of_request_sent',
                   'date_of_approval_of_candidates', 'desired_date_of_acceptance_from_agency',
                   'date_of_deployment_reported_from_agency', 'effective_date_of_deployment',
                   'date_of_closure_of_request', 'date_sent_to_supervisor', 'date_sent_to_validation']



class CreateRequest(BasicRequest):
    send_to_supervisor = forms.BooleanField(required=False, initial=False)  # initial force always return boolean field










