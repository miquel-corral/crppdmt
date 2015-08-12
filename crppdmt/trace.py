import sys
from django.core import serializers

from crppdmt.models import TraceAction

def trace_action(action_name, expert_request, person):
    try:
        new_log = TraceAction()
        new_log.action = action_name
        new_log.expert_request = expert_request
        if expert_request:
            new_log.description = serializers.serialize('xml', [expert_request])
        new_log.person = person
        new_log.save()
    except:
        print("Error tracing action: " + action_name)
        print("Error: " + str(sys.exc_info()))

