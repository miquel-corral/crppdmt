CHOICES_YES_NO = (
    ("YES", "YES"),
    ("NO", "NO")
)


CHOICES_DUTIES = (
    ("Key", "Key"),
    ("Other", "Other")
)


CHOICES_RECOMMENDATION = (
    ("SAME_TASKS", "Deployments with the same type of tasks as this one"),
    ("MORE_COMPLEX", "More complex and difficult tasks"),
    ("LESS_DEMANDING", "Less demanding tasks only"),
    ("DIFFERENT_AREA", "Tasks in a different technical area")
)


CHOICES_CONTACT_FREQUENCY = (
    ("Daily", "Daily"),
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    ("Less frequently", "Less frequently"),
)

ROLES = {
    "ROLE_CREATOR": 'Creator',
    "ROLE_COUNTRY_REPRESENTATIVE": 'Country Representative',
    "ROLE_SUPERVISOR": 'Supervisor',
    "ROLE_HQ_FOCAL_POINT": 'HQ Focal Point',
    "ROLE_FIELD_FOCAL_POINT": 'Field Focal Point',
    "ROLE_EXPERT": 'Expert',
}

ROLE_CREATOR_ITEM = "ROLE_CREATOR"
ROLE_COUNTRY_REPRESENTATIVE_ITEM = "ROLE_COUNTRY_REPRESENTATIVE"
ROLE_SUPERVISOR_ITEM = "ROLE_SUPERVISOR"
ROLE_HQ_FOCAL_POINT_ITEM = "ROLE_HQ_FOCAL_POINT"
ROLE_FIELD_FOCAL_POINT_ITEM = "ROLE_FIELD_FOCAL_POINT"
ROLE_EXPERT_ITEM = "ROLE_EXPERT"

################################################
#
# Help texts for forms
#
################################################

BACKGROUND_INFORMATION_HELP_TEXT = \
    "Current situation in country, existing programme strategies and mechanism, " \
    "current internal staffing capacity, staffing plans, other relevant information"

IF_OTHER_THAN_SUPERVISOR_HELP_TEXT = "Do not inform if same as supervisor"

PROFILE_SHELTER = "Shelter"

ToR_FIELDS_VALIDATION_ERROR = "All ToR fields must be informed."

################################################
#
# Presentation
#
################################################
ITEMS_PER_PAGE = 15


################################################
#
# Fields Names
#
################################################
ToR_FIELDS = 'ToR_fields'

################################################
#
# Workflow actions
#
################################################
ACTION_TO_SUPERVISOR = "to_supervisor"
ACTION_TO_VALIDATION = "to_validation"

################################################
#
# Email actions
#
################################################
MAIL_REQUEST_TO_REVIEW = "MAIL_REQUEST_TO_REVIEW"
MAIL_REQUEST_TO_VALIDATE  = "MAIL_REQUEST_TO_VALIDATE"
MAIL_REQUEST_VALIDATED_SUPERVISOR = "MAIL_REQUEST_VALIDATED_SUPERVISOR"
MAIL_REQUEST_VALIDATED_NORCAP = "MAIL_REQUEST_VALIDATED_NORCAP"
MAIL_REQUEST_NOT_VALIDATED = "MAIL_REQUEST_NOT_VALIDATED"

EMAIL_ADDRESS_NORCAP = "NRC@XXX.COM"


################################################
#
# Trace actions
#
################################################
TRACE_CREATE_REQUEST = "CREATE_REQUEST"
TRACE_EDIT_REQUEST = "EDIT REQUEST"
TRACE_VALIDATED_REQUEST = "VALIDATED REQUEST"
TRACE_NOT_VALIDATED_REQUEST = "NOT VALIDATED REQUEST"
TRACE_REQUEST_TO_SUPERVISOR = "REQUEST TO SUPERVISOR"
TRACE_VALIDATED_REQUEST_TO_SUPERVISOR = "VALIDATED_REQUEST_TO_SUPERVISOR"
TRACE_VALIDATED_REQUEST_TO_NORCAP = "VALIDATED REQUEST TO NORCAP"
TRACE_REQUEST_TO_VALIDATION = "REQUEST TO VALIDATION"

################################################
#
# Request status
#
################################################
STATUS_PREPARATION = "Preparation"
STATUS_SUPERVISION = "Supervision"
STATUS_VALIDATION = "Validation"
STATUS_CANDIDATE_APPROVAL = "Candidate Approval"
STATUS_DEPLOYMENT = "Deployment"
STATUS_MISSION_EXECUTION = "Mission Execution"
STATUS_PER_REVISION = "PER Revision"
STATUS_CLOSED = "Closed"