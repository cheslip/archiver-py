from django.forms.models import BaseInlineFormSet
from django import forms


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class LoginForm(forms.Form):
    username        = forms.CharField(label=(u'User Name'))
    password        = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
