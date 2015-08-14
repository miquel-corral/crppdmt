import os
from crppdmt.settings_private import TEST, EMAIL, MY_DEBUG, FTP, DEPLOY_ENV
from crppdmt.constants import ON, OFF, LOCAL, REMOTE


def test_is_in_state(state):
    return TEST == state


def test_is_on():
    return test_is_in_state(ON)


def test_is_off():
    return test_is_in_state(OFF)


def email_is_in_state(state):
    return state == os.getenv(EMAIL, OFF)


def email_is_on():
    return test_is_in_state(ON)


def email_is_off():
    return test_is_in_state(OFF)


def ftp_is_in_state(state):
    return state == os.getenv(FTP, OFF)


def ftp_is_on():
    return ftp_is_in_state(ON)


def ftp_is_off():
    return ftp_is_in_state(OFF)


def debug_is_in_state(state):
    return state == os.getenv(state, OFF)


def debug_is_on():
    return test_is_in_state(ON)


def debug_is_off():
    return test_is_in_state(OFF)


def env_is(environment):
    return environment == DEPLOY_ENV


def env_is_remote():
    return env_is(REMOTE)


def env_is_local():
    return env_is(LOCAL)




