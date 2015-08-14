import os
from crppdmt.settings import TEST, EMAIL, FTP, DEPLOY_ENV, MY_DEBUG
from crppdmt.constants import ON, OFF, LOCAL, REMOTE


def test_is_in_state(state):
    return TEST == state


def test_is_on():
    return test_is_in_state(ON)


def test_is_off():
    return test_is_in_state(OFF)


def email_is_in_state(state):
    return EMAIL == state


def email_is_on():
    return email_is_in_state(ON)


def email_is_off():
    return email_is_in_state(OFF)


def ftp_is_in_state(state):
    return FTP == state


def ftp_is_on():
    return ftp_is_in_state(ON)


def ftp_is_off():
    return ftp_is_in_state(OFF)


def debug_is_in_state(state):
    return MY_DEBUG == state


def debug_is_on():
    return debug_is_in_state(ON)


def debug_is_off():
    return debug_is_in_state(OFF)


def env_is(environment):
    return environment == DEPLOY_ENV


def env_is_remote():
    return env_is(REMOTE)


def env_is_local():
    return env_is(LOCAL)




