import os
import django.db.models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime
from django.utils import timezone

from crppdmt.constants import *
from crppdmt.validators import validate_date_greater_than_today


class Common(django.db.models.Model):
    """
    Abstract base class
    """
    # ...

    class Meta:
        abstract = True


class BasicName(Common):
    """
    Abstract base class for entities with single "name" field
    """
    name = django.db.models.CharField(max_length=250, null=False, blank=False, unique=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Country(BasicName):
    """
    Represents countries
    """

class MissionStatus(BasicName):
    """
    Represents mission status
    """


class Organization(BasicName):
    """
    Represents an organization in the system
    """
    type = django.db.models.CharField(max_length=25, null=False, blank=False)

class Role(BasicName):
    """
    Represents a functional role
    """


class Person(BasicName):
    """
    Represents UN-Habitat Staff
    """
    title = django.db.models.CharField(max_length=100, null=True, blank=True)
    phone_no = django.db.models.CharField(max_length=50, null=True, blank=True)
    email = django.db.models.CharField(max_length=100, null=False, blank=False,validators=[validate_email,])
    organization = django.db.models.ForeignKey(Organization)
    organization_number = django.db.models.CharField(max_length=20, null=True, blank=True)
    un_habitat_number = django.db.models.CharField(max_length=20, null=True, blank=True, verbose_name='UN-Habitat ID')
    roles = django.db.models.ManyToManyField(Role)
    user = django.db.models.ForeignKey(User)
    first_name = django.db.models.CharField(max_length=100, null=False, blank=False)
    last_name = django.db.models.CharField(max_length=100, null=True, blank=True)
    personal_title = django.db.models.CharField(max_length=5, null=True, blank=True)
    certifier = django.db.models.ForeignKey(User, null=True, blank=True, related_name='Certifier')

    def can_create(self):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES[ROLE_SUPERVISOR_ITEM] or role.name == ROLES[ROLE_CREATOR_ITEM]:
                ret = True
                break
        return ret

    def can_validate(self):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES[ROLE_COUNTRY_REPRESENTATIVE_ITEM]:
                ret = True
                break
        return ret

    def can_validate_user(self):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES[ROLE_COUNTRY_REPRESENTATIVE_ITEM]:
                ret = True
                break
        return ret

    def has_role(self, role_name):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES[role_name]:
                ret = True
                break
        return ret

    def is_supervisor(self):
        return self.has_role(ROLE_SUPERVISOR_ITEM)

    def is_expert(self):
        return self.has_role(ROLE_EXPERT_ITEM)


class RequestStatus(BasicName):
    """
    Represents request for personnel status
    """


class ExpertProfileType(BasicName):
    """
    Represents an expert profile type
    """


class ExpertRequest(BasicName):
    """
    Represents a request to an external agency
    """

    def validate_file_size(file_field):
        if os.path.isfile(file_field.name):
            file_size = file_field.file.size
            megabyte_limit = 2.0
            if file_size > megabyte_limit*1024*1024:
                os.remove(file_field.name)
                raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    def validate_file_format(file_field):
        if os.path.isfile(file_field.name):
            dot_position = file_field.name.find('.')
            if (dot_position == -1):
                raise ValidationError(u'File type not supported! ')

            ext = file_field.name[dot_position:len(file_field.name)]
            valid_extensions = ['.pdf']

            if not ext in valid_extensions:
                os.remove(file_field.name)
                raise ValidationError(u'File type not supported! ' + ext)

    # expert profile type
    expert_profile_type = django.db.models.ForeignKey(ExpertProfileType, null=True, blank=True)
    # control data
    status = django.db.models.ForeignKey(RequestStatus, null=False, blank=False)
    date_of_request_sent = django.db.models.DateField(null=True, blank=True)
    date_of_approval_of_candidates = django.db.models.DateField(null=True, blank=True)
    desired_date_of_acceptance_from_agency = django.db.models.DateField(null=True, blank=True)
    date_of_deployment_reported_from_agency = django.db.models.DateField(null=True, blank=True)
    effective_date_of_deployment = django.db.models.DateField(null=True, blank=True)
    date_of_closure_of_request = django.db.models.DateField(null=True, blank=True)
    date_sent_to_supervisor = django.db.models.DateField(null=True, blank=True)
    date_sent_to_validation = django.db.models.DateField(null=True, blank=True)
    # basic information
    title = django.db.models.CharField(max_length=100, null=False, blank=False, verbose_name="Job Title")
    project_name = django.db.models.CharField(max_length=100, null=False, blank=False)
    project_code = django.db.models.CharField("Project/Budget code", max_length=100, null=False, blank=False)
    project_document = django.db.models.FileField(null=True, blank=True, validators=[validate_file_format, validate_file_size], verbose_name="Project Description Document")
    requesting_agency = django.db.models.CharField(max_length=100, null=False, blank=False, default="UN-HABITAT")
    requested_agency = django.db.models.ForeignKey(Organization, null=False, blank=False, default="NORCAP")
    country = django.db.models.ForeignKey(Country, null=True, blank=True)
    duty_station = django.db.models.CharField(max_length=250, null=False, blank=False)
    requested_date_of_deployment = django.db.models.DateField(null=False, blank=False, validators=[validate_date_greater_than_today])
    security_phase_in_duty_station = django.db.models.CharField(max_length=50, null=False, blank=False, default="NA")
    requested_length_of_deployment = django.db.models.CharField(max_length=50, null=False, blank=False)
    first_request = django.db.models.CharField(max_length=5, choices=CHOICES_YES_NO, null=False, blank=False)
    extension = django.db.models.CharField(max_length=5, null=False, blank=False)
    # People
    request_creator = django.db.models.ForeignKey(Person, related_name="REQCreator")
    country_representative = django.db.models.ForeignKey(Person, related_name="REQCountryRepresentative")
    supervisor = django.db.models.ForeignKey(Person, related_name="REQSupervisor")
    agency_hq_focal_point = django.db.models.ForeignKey(Person, related_name="REQAgencyHQFocalPoint", null=True, blank=True, verbose_name="Agency HQ focal point")
    agency_field_focal_point = django.db.models.ForeignKey(Person, related_name="REQAgencyFieldFocalPoint", null=True, blank=True)
    expert = django.db.models.ForeignKey(Person, null=True, blank=True)
    # Background information/reason for request or extent
    background_information = django.db.models.TextField(null=True, blank=True)
    # ToR data
    objectives_and_scope = django.db.models.TextField(null=True, blank=True)
    expert_profile = django.db.models.TextField(null=True, blank=True)
    expected_outputs = django.db.models.TextField(null=True, blank=True)
    main_duties_and_responsibilities = django.db.models.TextField(null=True, blank=True)
    other_relevant_information = django.db.models.TextField(null=True, blank=True)
    # Rejection
    rejected_review_date = django.db.models.DateField(null=True, blank=True)
    rejected_review_reason = django.db.models.TextField(null=True, blank=True)
    rejected_certification_date = django.db.models.DateField(null=True, blank=True)
    rejected_certification_reason = django.db.models.TextField(null=True, blank=True)

    def clean(self):
        # Control supervisor and country representative not the same person
        # control deleted in order to have the possibility to have it open
        """
        if hasattr(self, 'supervisor') and hasattr(self, 'country_representative'):
            if self.supervisor == self.country_representative:
                raise ValidationError('Country Representative and Supervisor must be different.')
        """

    def has_empty_text_fields(self):
        if self.background_information == '':
            return True
        if self.objectives_and_scope == '':
            return True
        if self.expert_profile == '':
            return True
        if self.main_duties_and_responsibilities == '':
            return True
        if self.other_relevant_information == '':
            return True
        return False

    def has_no_changed_text_fields(self):
        if self.background_information == BACKGROUND_INFORMATION_HELP_TEXT + "\n" + PLEASE_DETAIL_HELP_TEXT:
            return True
        if self.objectives_and_scope == PLEASE_DETAIL_HELP_TEXT:
            return True
        if self.expert_profile == PLEASE_DETAIL_HELP_TEXT:
            return True
        if self.main_duties_and_responsibilities == PLEASE_DETAIL_HELP_TEXT:
            return True
        if self.other_relevant_information == PLEASE_DETAIL_HELP_TEXT:
            return True
        return False

    def is_in_status(self, status_name):
        return self.status.name == status_name

    def is_in_status_execution(self):
        return self.is_in_status(STATUS_MISSION_EXECUTION)

    def is_in_status_deployment(self):
        return self.is_in_status(STATUS_DEPLOYMENT)

    def is_in_status_closed(self):
        return self.is_in_status(STATUS_CLOSED)


class Duty(BasicName):
    """
    Represents a duty
    """
    type = django.db.models.CharField(max_length=10, choices=CHOICES_DUTIES, null=False, blank=False)


class ToR(BasicName):
    """
    Represents a ToR
    """
    post = django.db.models.CharField(max_length=250, null=False, blank=False)
    duty_station = django.db.models.CharField(max_length=250, null=False, blank=False)
    term = django.db.models.CharField(max_length=100, null=False, blank=False)
    background = django.db.models.CharField(max_length=500, null=False, blank=False)
    objectives = django.db.models.CharField(max_length=500, null=False, blank=False)
    key_duties = django.db.models.ManyToManyField(Duty, related_name="ToRKeyDuties")
    other_duties = django.db.models.ManyToManyField(Duty, related_name="ToROtherDuties")
    qualifications = django.db.models.TextField(null=False, blank=False)


class AttendanceCode(BasicName):
    """
    Represents an attendance code
    """


class MonthlyReport(BasicName):
    """
    Represents a monthly report
    """
    expert_request = django.db.models.ForeignKey(ExpertRequest)
    expert = django.db.models.ForeignKey(Person, related_name="MRExpert")
    project_number = django.db.models.CharField(max_length=20, null=True, blank=True)
    month_year = django.db.models.CharField(max_length=7, null=False, blank=False)
    date_of_expert_report = django.db.models.DateField(null=True, blank=True)
    supervisor = django.db.models.ForeignKey(Person, related_name="MRSupervisor")
    date_of_approval_of_supervisor = django.db.models.DateField(null=True, blank=True)
    date_report_sent = django.db.models.DateField(null=True, blank=True)


class MonthlyReportRecord(Common):
    """
    Represents a record of the monthly report
    """
    day_number = django.db.models.CharField(max_length=2, null=False, blank=False)
    attendance_code = django.db.models.ForeignKey(AttendanceCode)
    place_of_duty = django.db.models.CharField(max_length=100, null=False, blank=False)
    monthly_report = django.db.models.ForeignKey(MonthlyReport)


class PER(Common):
    """
    Represents a performance evaluation report
    """
    # general info
    expert_request = django.db.models.ForeignKey(ExpertRequest)
    expert = django.db.models.ForeignKey(Person, related_name="PERExpert")
    date_of_expert_report = django.db.models.DateField(null=True, blank=True)
    supervisor = django.db.models.ForeignKey(Person, related_name="PERSupervisor")
    date_of_approval_of_supervisor = django.db.models.DateField(null=True, blank=True)
    date_report_sent = django.db.models.DateField(null=True, blank=True)
    # basic information block
    post_title = django.db.models.CharField(max_length=100, null=False, blank=False)
    duty_station = django.db.models.CharField(max_length=250, null=False, blank=False)
    un_host_agency = django.db.models.CharField(max_length=250, null=False, blank=False)
    seconding_agency = django.db.models.CharField(max_length=250, null=False, blank=False)
    function = django.db.models.TextField(null=False, blank=False)
    period_of_deployment = django.db.models.CharField(max_length=250, null=True, blank=True)
    # key assignments and outputs block in another entity
    # impact and sustainability block
    impact = django.db.models.TextField(null=True, blank=True)
    sustainability = django.db.models.TextField(null=True, blank=True)
    effect = django.db.models.TextField(null=True, blank=True)
    # professional competences in another entity
    recommendation = django.db.models.CharField(max_length=10, choices=CHOICES_RECOMMENDATION, null=True, blank=True)
    recommendation_explanation = django.db.models.TextField(null=True, blank=True)
    recommended_competence_development = django.db.models.TextField(null=True, blank=True)
    # general comments
    general_comments = django.db.models.TextField(null=True, blank=True)
    frequency_of_contact = django.db.models.CharField(max_length=20, choices=CHOICES_CONTACT_FREQUENCY, null=True,
                                                      blank=True)
    technical_focal_point = django.db.models.ForeignKey(Person)
    # expert review block
    agree_with_evaluation = django.db.models.CharField(max_length=5, choices=CHOICES_YES_NO, null=True, blank=True)
    general_comments_expert = django.db.models.TextField(null=True, blank=True)
    competence_development = django.db.models.TextField(null=True, blank=True)



class AlertType(BasicName):
    """
    Represents an alert type
    """


class AlertStatus(BasicName):
    """
    Represents alert status
    """


class Alert(Common):
    """
    Represents an alert
    """
    type = django.db.models.ForeignKey(AlertType)
    status = django.db.models.ForeignKey(AlertStatus)
    date_raised = django.db.models.DateField(null=False, blank=False)
    date_sent = django.db.models.DateTimeField(null=False, blank=False)
    expert_request = django.db.models.ForeignKey(ExpertRequest)


class Statistic(Common):
    """
    Represents an statistic record
    """
    year = django.db.models.CharField(max_length=4, null=False, blank=False)
    number_of_missions = django.db.models.IntegerField(blank=False, null=False)
    number_of_requests = django.db.models.IntegerField(blank=False, null=False)
    number_of_missions_closed = django.db.models.IntegerField(blank=False, null=False)
    number_of_missions_closed_no_issues = django.db.models.IntegerField(blank=False, null=False)


class GeneralCheckList(Common):
    """
    Represents questions of general check list
    """
    article_description = django.db.models.CharField(max_length=250, null=True, blank=True)
    article_number = django.db.models.CharField(max_length=250, null=True, blank=True)
    duties_and_responsibilities = django.db.models.TextField(null=False, blank=False)


class TraceAction(Common):
    """
    Represents an action traced by the system
    """
    action = django.db.models.CharField(max_length=50, null=False, blank=False)
    description = django.db.models.TextField(null=False, blank=False)
    person = django.db.models.ForeignKey(Person)
    date = django.db.models.DateTimeField(default=timezone.now, null=False, blank=False)
    expert_request = django.db.models.ForeignKey(ExpertRequest, null=True, blank=True)


class PersonalDocument(Common):
    """
    Represents a personal document from an expert
    """

    def validate_file_size(file_field):
        if os.path.isfile(file_field.name):
            file_size = file_field.file.size
            megabyte_limit = 2.0
            if file_size > megabyte_limit*1024*1024:
                os.remove(file_field.name)
                raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    def validate_file_format(file_field):
        if os.path.isfile(file_field.name):
            dot_position = file_field.name.find('.')
            if (dot_position == -1):
                raise ValidationError(u'File type not supported! ')

            ext = file_field.name[dot_position:len(file_field.name)]
            valid_extensions = ['.pdf']

            if not ext in valid_extensions:
                os.remove(file_field.name)
                raise ValidationError(u'File type not supported! ' + ext)


    file_name = django.db.models.FileField(upload_to='./', null=False, blank=False, validators=[validate_file_format,
                                                                                                validate_file_size])
    document_title = django.db.models.CharField(max_length=50, null=True, blank=True)
    expert = django.db.models.ForeignKey(Person, null=False, blank=False)


class ExpertMessage(Common):
    """
    Represents a personal document from an expert
    """
    subject = django.db.models.CharField(max_length=50, null=False, blank=False)
    message = django.db.models.CharField(max_length=500, null=False, blank=False)
    expert = django.db.models.ForeignKey(Person, null=False, blank=False)
    expert_request = django.db.models.ForeignKey(ExpertRequest, null=True, blank=True)
