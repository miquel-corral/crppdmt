from django import forms
from crppdmt.constants import CHOICES_YES_NO

############################################################
#
# Helper functions form fields presentation
#
#############################################################


def set_form_hidden_fields(formset, fields_to_show):
    """
    Function to set hidden fields and show fields of each form in formset
    :param formset:
    :param files_to_show:
    :return:
    """
    for form in formset:
        for field in form.fields:
            if not any(field in s for s in fields_to_show):
                form.fields[field].widget = forms.HiddenInput()


def set_form_hidden_fields_hidden_fields(formset, fields_to_hide):
    """
    Function to set hidden fields and show fields of each form in formset
    :param formset:
    :param files_to_show:
    :return:
    """
    for form in formset:
        for field in form.fields:
            if field in fields_to_hide:
                form.fields[field].widget = forms.HiddenInput()


def set_form_readonly_fields(formset, read_only_fields):
    """
    Function to set readonly fields of each form in formset
    :param formset:
    :return:
    """
    for form in formset:
        for field in form.fields:
            print(field)
            if any(field in s for s in read_only_fields):
                print(field)
                form.fields[field].widget.attrs['disabled'] = True


def set_form_country_select(formset):
    for form in formset:
        for field in form.fields:
            print(field)
            fields_to_change = ('country')
            if any (field in s for s in fields_to_change):
                #form.fields[field] = forms.MultipleChoiceField(choices=CHOICES_YES_NO, blank=True)
                # This works to change choices: form.fields[field].widget.attrs['choices'] = CHOICES_YES_NO
                form.fields[field].widget = forms.Select(choices=CHOICES_YES_NO)


