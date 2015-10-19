# ###############################################
#
# Choices
#
################################################
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


# ###############################################
#
# User roles
#
################################################
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


# ###############################################
#
# Organization types
#
################################################

ORGANIZATION_TYPE_REQUESTING = "REQUESTING"
ORGANIZATION_TYPE_REQUESTED = "REQUESTED"


# ###############################################
#
# Help texts for forms
#
################################################

BACKGROUND_INFORMATION_HELP_TEXT = \
    "Current situation in country, existing programme strategies and mechanism, " \
    "current internal staffing capacity, staffing plans, other relevant information."

PLEASE_DETAIL_HELP_TEXT = "Please describe"

IF_OTHER_THAN_SUPERVISOR_HELP_TEXT = "Do not inform if same as supervisor"

PROFILE_SHELTER = "Shelter"

ToR_FIELDS_VALIDATION_ERROR = "All ToR fields must be filled."
REJECT_REASON_VALIDATION_ERROR = "Rejection Reason must be filled"

################################################
#
# Profile Types
#
################################################
PROFILE_FOOD_SECURITY = "Food Security"
PROFILE_DRR = "DRR"
PROFILE_SHELTER = "Shelter"
PROFILE_ENGINEERING = "Engineering"
PROFILE_WATER = "Water"
PROFIlE_EDUCATION ="Education"
PROFILE_SANITATON = "Sanitation"
PROFILE_NUTRITION = "Nutrition"
PROFILE_HEALTH = "Health"
PROFILE_COMMUNICATION = "Communication"
PROFILE_COORDINATION = "Coordination"
PROFILE_STATISTICS = "Statistics"
PROFILE_CHILD_PROTECTION = "Child Protection"
PROFILE_GENDER = "Gender"
PROFILE_CAMP_COORDINATION = "Camp Coordination"
PROFILE_HOUSING = "Housing"
PROFILE_ICT = "ICT"
PROFILE_LOGISTICS = "Logistics"
PROFILE_INFORMATION_MANAGEMENT = "Information Management"
PROFILE_PROJECT_FORMULATION = "Project Formulation"


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
REJECT_REASON = 'reject_reason'

################################################
#
# Workflow actions
#
################################################
ACTION_TO_SUPERVISOR = "to_supervisor"
ACTION_TO_CERTIFICATION = "to_certification"

################################################
#
# Email actions
#
################################################
MAIL_REQUEST_TO_REVIEW = "MAIL_REQUEST_TO_REVIEW"
MAIL_REQUEST_TO_CERTIFY = "MAIL_REQUEST_TO_CERTIFY"
MAIL_REQUEST_CERTIFIED = "MAIL_REQUEST_CERTIFIED"
MAIL_REQUEST_NOT_REVIEWED = "MAIL_REQUEST_NOT_REVIEWED"
MAIL_REQUEST_NOT_CERTIFIED = "MAIL_REQUEST_NOT_CERTIFIED"
MAIL_USER_REGISTERED = "MAIL_USER_REGISTERED"
MAIL_USER_VALIDATED = "MAIL_USER_VALIDATED"
MAIL_USER_REJECTED = "MAIL_USER_REJECTED"
MAIL_CANDIDATE_APPROVED = "MAIL_CANDIDATE_APPROVED"
MAIL_EXPERT_REGISTERED = "MAIL_EXPERT_REGISTERED"
MAIL_EXPERT_MESSAGE = "MAIL_EXPERT_MESSAGE"


################################################
#
# Trace actions
#
################################################
TRACE_CREATE_REQUEST = "CREATE REQUEST"
TRACE_EDIT_REQUEST = "EDIT REQUEST"
TRACE_VALIDATED_REQUEST = "VALIDATED REQUEST"
TRACE_NOT_VALIDATED_REQUEST = "NOT VALIDATED REQUEST"
TRACE_REQUEST_TO_SUPERVISOR = "REQUEST TO SUPERVISOR"
TRACE_VALIDATED_REQUEST_TO_SUPERVISOR = "VALIDATED REQUEST TO SUPERVISOR"
TRACE_VALIDATED_REQUEST_TO_NORCAP = "VALIDATED REQUEST TO NORCAP"
TRACE_REQUEST_TO_CERTIFICATION = "REQUEST TO CERTIFICATION"
TRACE_COPIED_REQUEST = "REQUEST COPIED"
TRACE_EXTENDED_REQUEST = "REQUEST EXTENDED"
TRACE_REJECTED_REVIEW_REQUEST = "REQUEST REVIEW REJECTED"
TRACE_REJECTED_CERTIFICATION_REQUEST = "REQUEST CERTIFICATION REJECTED"
TRACE_USER_REGISTERED = "USER REGISTERED"
TRACE_USER_VALIDATED = "USER VALIDATED"
TRACE_USER_REJECTED = "USER REJECTED"
TRACE_CANDIDATE_APPROVED = "CANDIDATE APPROVED"
TRACE_EXPERT_CREATED = "EXPERT CREATED"
TRACE_DEPLOYMENT_DATE_SET = "DEPLOYMENT_DATE_SET"

################################################
#
# Request status
#
################################################
STATUS_PREPARATION = "Preparation"
STATUS_SUPERVISION = "Supervision"
STATUS_CERTIFICATION = "Certification"
STATUS_CANDIDATE_APPROVAL = "Candidate Approval"
STATUS_DEPLOYMENT = "Deployment"
STATUS_MISSION_EXECUTION = "Mission Execution"
STATUS_PER_REVISION = "PER Revision"
STATUS_CLOSED = "Closed"

################################################
#
# Control constants for env. and status of subsystems
#
################################################
REMOTE = "REMOTE"
LOCAL = "LOCAL"
ON="ON"
OFF="OFF"

