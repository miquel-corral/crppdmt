# from __future__ import unicode_literals

import csv
import sys
import os


import datetime

from django.conf import settings

project_path = "/Users/miquel/UN/0003-CRPTDEV/crppdmt/"
sys.path.append(project_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'crppdmt.settings'


# OBS: to initialize Django in 1.7 and run python scripts. Do not include 'setup' in installed_apps
import django
django.setup()

from django.contrib.auth.models import User, Group
from crppdmt.models import *
from crppdmt.my_old_ftp import MyFTP

def load_users_file():
    """
    Load into database users for cities in users.csv file
    :return:
    """
    print("load_users_file. Start..")
    file_path = settings.BASE_DIR + "/files/users.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # read data from line
        username = row[0].strip()
        pwd = row[1].strip()
        email = row[2].strip()
        group_name = row[3].strip()
        first_name = row[4].strip()
        last_name = row[5].strip()
        # check before creation
        try:
            user = User.objects.get(username=username)
            print("User yet exists: " + row[0].strip())
        except:
            print("User does not exist: " + row[0].strip())
            user = User.objects.create_user(username, email, pwd)
        # create/update  user and eventually new group
        try:
            group = get_user_group(group_name)

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user.groups.add(group)
        except:
            print("Error creating user: " + username)
            print("Unexpected error:", sys.exc_info())
    print("load_users_file. End....")


def get_user_group(group_name):
    """
    gets or create a user group
    :param group_name:
    :return:
    """
    try:
        group = Group.objects.get(name=group_name)
        return group
    except:
        print("Group does not exist: " + group_name)
        try:
            group = Group()
            group.name = group_name
            group.save()
            print("Group created: " + group_name)
            return group
        except:
            print("Error creating group: " + group_name)


def load_entity_single_field_name(file_name, class_name):
    """
    Load file of entities with a single field name
    :param file_name:
    :param class_name:
    :return:
    """
    print("load_entity_single_field_name: " + file_name + " .Start...")
    file_path = settings.BASE_DIR + "/files/" + file_name
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    for row in data_reader:
        entity = class_name()
        entity.name = row[0].strip()
        try:
            entity.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_entity_single_field_name: " + file_name + " .End.")


def load_requests():
    """
    Load requests file
    :return:
    """
    print("load_requests. Start...")
    file_path = settings.BASE_DIR + "/files/" + "requests.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        try:
            request = ExpertRequest()
            request.name = row[0].strip()
            request.requesting_agency = Organization.objects.get(name=row[1].strip())
            request.country = row[2].strip()
            request.duty_station = row[3].strip()
            request.requested_date_of_deployment = datetime.datetime.strptime(row[4].strip(),'%d/%m/%Y')
            request.security_phase_in_duty_station = "NA"
            request.requested_length_of_deployment = "3 months"
            request.first_request = row[5].strip()
            user = User.objects.get(username=row[6].strip())
            request.country_representative = Person.objects.get(user=user)
            user = User.objects.get(username=row[7].strip())
            request.request_creator = Person.objects.get(user=user)
            request.supervisor = Person.objects.get(user=user)
            user = User.objects.get(username=row[8].strip())
            request.agency_hq_focal_point = Person.objects.get(user=user)
            user = User.objects.get(username=row[9].strip())
            request.agency_field_focal_point = Person.objects.get(user=user)
            request.status = RequestStatus.objects.get(name='Preparation')
        except:
            print("Unexpected error:", sys.exc_info())

        print("Request: " + request.name)
        try:
            request.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_requests. End.")


def load_people():
    """
    Load persons file
    :return:
    """
    print("load_people. Start...")
    file_path = settings.BASE_DIR + "/files/" + "people.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip headers row
    for row in data_reader:
        # check if user exists. if not trace and skip row
        try:
            try:
                user = User.objects.get(username=row[6].strip())
                print("username: " + row[6].strip())
            except:
                print("User does not exist: " + row[6].strip())
                print("Unexpected error:", sys.exc_info())

            # check if person exists to update it. If not, create it
            try:
                person = Person.objects.get(user=user)
                print("Person exists: " + person.name)
            except:
                print("Person does not exist: " + user.username)
                person = Person()
            person.title = row[0].strip()
            person.phone_no = row[1].strip()
            person.email = row[2].strip()
            person.organization = Organization.objects.get(name=row[3].strip())
            person.organization_number = row[4].strip()
            person.un_habitat_number = row[5].strip()
            person.personal_title = row[7].strip()
            person.first_name = row[8].strip()
            person.last_name = row[9].strip()
            person.name = person.last_name + ", " + person.first_name
            # update user
            person.user = user
            person.save()
            # update roles
            for i in range(10,15):
                try:
                    person.roles.add(Role.objects.get(name=row[i].strip()))
                    person.save()
                except:
                    pass
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_people. End.")


def load_general_checklist():
    """
    load general checklist questions file
    """
    print("load_general_checklist. Start...")
    file_path = settings.BASE_DIR + "/files/general_checklist.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip column headers
    for row in data_reader:
        question = GeneralCheckList()
        question.article_description = row[0].strip()
        question.article_number = row[1].strip()
        question.duties_and_responsibilities = row[2].strip()
        try:
            question.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_general_checklist. End.")


def load_organizations():
    """
    load organizations file
    """
    print("load_organizations. Start...")
    file_path = settings.BASE_DIR + "/files/organizations.tsv"
    data_reader = csv.reader(open(file_path), dialect='excel-tab')
    data_reader.next()  # to skip column headers
    for row in data_reader:
        organization = Organization()
        organization.name = row[0].strip()
        organization.type = row[1].strip()
        try:
            organization.save()
        except:
            print("Unexpected error:", sys.exc_info())
    print("load_organizations. End.")


if __name__ == "__main__":
    load_entity_single_field_name("countries.tsv", Role)
    load_entity_single_field_name("roles.tsv", Role)
    load_organizations()
    load_users_file()
    load_people()
    load_entity_single_field_name("mission_status.tsv", MissionStatus)
    load_entity_single_field_name("alert_status.tsv", AlertStatus)
    load_entity_single_field_name("alert_types.tsv", AlertType)
    load_entity_single_field_name("request_status.tsv", RequestStatus)
    load_entity_single_field_name("expert_profile_type.tsv", ExpertProfileType)
    load_general_checklist()
    load_entity_single_field_name("countries.tsv", Country)







