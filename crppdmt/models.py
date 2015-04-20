import django.db.models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from crppdmt.validators import *

from crppdmt.constants import CHOICES_YES_NO, CHOICES_DUTIES, CHOICES_RECOMMENDATION, CHOICES_CONTACT_FREQUENCY, ROLES


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


class MissionStatus(BasicName):
    """
    Represents mission status
    """


class Organization(BasicName):
    """
    Represents an organization in the system
    """


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
    email = django.db.models.CharField(max_length=100, null=False, blank=False)
    organization = django.db.models.ForeignKey(Organization)
    organization_number = django.db.models.CharField(max_length=20, null=True, blank=True)
    un_habitat_number = django.db.models.CharField(max_length=20, null=True, blank=True)
    roles = django.db.models.ManyToManyField(Role)
    user = django.db.models.ForeignKey(User)
    first_name = django.db.models.CharField(max_length=100, null=False, blank=False)
    last_name = django.db.models.CharField(max_length=100, null=True, blank=True)
    personal_title = django.db.models.CharField(max_length=5, null=True, blank=True)

    def can_create(self):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES["ROLE_SUPERVISOR"] or role.name == ROLES["ROLE_CREATOR"]:
                ret = True
                break
        return ret

    def can_validate(self):
        ret = False
        for role in self.roles.all():  # everyone has at least one role
            if role.name == ROLES["ROLE_COUNTRY_REPRESENTATIVE"]:
                ret = True
                break
        return ret



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
    project_name = django.db.models.CharField(max_length=100, null=False, blank=False)
    project_code = django.db.models.CharField("Project/Budget code", max_length=100, null=False, blank=False)
    project_document = django.db.models.FileField(null=True, blank=True, validators=[validate_file_extension, validate_file_size])
    requesting_agency = django.db.models.CharField(max_length=100, null=False, blank=False, default="UN-HABITAT")
    country = django.db.models.CharField(max_length=250, null=False, blank=False)
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


    def clean(self):
        # Control supervisor and country representative not the same person
        if self.supervisor == self.country_representative:
            raise ValidationError('Country Representative and Supervisor must be different.')

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
    request = django.db.models.ForeignKey(ExpertRequest)

