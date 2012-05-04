from django import forms
from accounts.models import Account, Settings
from boxes.models import BoxItem
from django.forms import ModelForm

NUMBER_CHOICES = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class SingleArchiveForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label=(u'Select Account'), required=True)
    accession = forms.CharField(label=(u'Accession'), required=True)

class BatchArchiveForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label=(u'Select Account'))
    accessions = forms.CharField(label=(u'Accessions'), widget=forms.Textarea)


    def clean_accessions(self):
        """ Checks to see if accessions are all exactly 8 characters long
            Raise validation error if otherwise
        """
        data = self.cleaned_data['accessions']

        # Tidy up accessions from form text area
        accessions_list = data.split('\r\n')
        accessions_list = filter(None, accessions_list)

        for accession in accessions_list:
            if len(str(accession)) != 8:
                raise forms.ValidationError("All accessions must be 8 characters long")

        return data


class ArchiveForm(forms.Form):
    serum = forms.ChoiceField(choices=NUMBER_CHOICES, initial=1)
    plasma = forms.ChoiceField(choices=NUMBER_CHOICES, initial=1)
    donor_id = forms.CharField(label=(u'Donor ID'), required=False)
    
#    def clean_donor_id(self):
        
#        data = self.cleaned_data['donor_id']
#        print "DATA: " + str(data)
#        
#        if not data:
#            print "SHIT"
#           raise forms.ValidationError('You must enter a donor ID')
#           
#       
#       return data


class ListForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.all().order_by('name'), empty_label=(u'Select Account'), required=True)
    number = forms.IntegerField(label=(u'Box Number'), required=True)