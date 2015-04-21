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
    "ROLE_CREATOR":'Creator',
    "ROLE_COUNTRY_REPRESENTATIVE": 'Country Representative',
    "ROLE_SUPERVISOR": 'Supervisor',
    "ROLE_HQ_FOCAL_POINT": 'HQ Focal Point',
    "ROLE_FIELD_FOCAL_POINT": 'Field Focal Point',
    "ROLE_EXPERT": 'Expert',
}

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

################################################
#
# Presentation
#
################################################
ITEMS_PER_PAGE = 15



