from crppdmt.models import Person, RequestStatus, User, Organization, ExpertRequest
from crppdmt.mail_utils import *
from crppdmt.constants import *
from crppdmt.shelter_tor import *

############################################
#
# Helper functions to manage users and permissions
#
############################################


def create_person_and_user(person, role=None, is_active=False, initial_pwd=True):
    """
    Function to create a new person and associate user with data from template form
    :param person:
    :param initial_pwd:
    :return:
    """

    print(person.name)
    print(person.last_name)
    print(person.title)

    person.first_name = person.first_name.replace(" ", "_")
    person.last_name = person.last_name.replace(" ", "_")
    # set person additional information
    person.name = person.last_name + ", " + person.first_name
    # create user deactivated, person after and then set role creator
    username = (person.first_name.lower().strip() + "." + person.last_name.lower().strip()).replace(" ", "")

    if initial_pwd:
        password = "0304" + person.last_name
    else:
        password=None

    user = User.objects.create_user(username, person.email, password)
    user.first_name = person.first_name
    user.last_name = person.last_name
    user.email = person.email
    user.is_active = is_active
    user.is_staff = False
    user.is_superuser = False
    user.save()
    person.user = user
    person.save()

    if role:
        person.roles.add(role)
    person.save()
    # trace & send email
    if role and role.name == ROLE_EXPERT_ITEM:
        person.organization = Organization.objects.get(name='NORCAP').id
        person.save()
        trace_action(TRACE_EXPERT_CREATED,None,person)
        send_new_expert_email(person, person.supervisor)


def get_person_by_username(username):
    """
    Get person by username
    :param username:
    :return:
    """
    user = get_user_by_username(username)
    if user:
        return get_person_by_user(user)
    else:
        return None


def get_person_by_user(user):
    """
    Get person by username
    :param username:
    :return:
    """
    if user:
        try:
            person = Person.objects.get(user=user)
        except:
            person = None
        return person
    else:
        return None

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


def supervisor_can_access_expert_profile(supervisor, expert):
    try:
        # get open deployment of expert
        expert_request_list = ExpertRequest.objects.filter(expert=expert, status__in=[STATUS_DEPLOYMENT,
                                                                                      STATUS_MISSION_EXECUTION,
                                                                                      STATUS_PER_REVISION])
        # check requests list
        num_requests = len(expert_request_list)
        if num_requests == 0 or num_requests > 1:
            return False;
        expert_request = expert_request_list[0]
        # check if supervisor matches
        return expert_request.supervisor == supervisor
    except:
        return False


############################################
#
# Helper functions to manage expert requests
#
############################################


def link_expert_id_to_request(expert_request, expert_id):
    """
    Function to set expert for given request
    :param expert_request:
    :param expert_id:
    :return:
    """
    # get expert
    expert = Person.objects.get(id=expert_id)
    link_expert_to_request(expert_request, expert)


def link_expert_to_request(expert_request, expert):
    """
    Function to set expert for given request
    :param expert_request:
    :param expert:
    :return:
    """
    # link to request and change status
    expert_request.expert = expert
    expert_request.status = RequestStatus.objects.get(name=STATUS_DEPLOYMENT)
    expert_request.save()
    # send email
    send_request_email_to(expert_request, MAIL_CANDIDATE_APPROVED)
    # trace
    trace_action(TRACE_CANDIDATE_APPROVED,expert_request,expert_request.supervisor)


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


