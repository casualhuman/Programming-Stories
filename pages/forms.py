
from django import forms 
from .models import ReportProblem
from django.utils.translation import gettext_lazy as _



class ReportProblemForm(forms.ModelForm):
    class Meta:
        model = ReportProblem
        exclude = ('date_reported',)


        widgets = {
            'problem': forms.Textarea(attrs={'placeholder': 'Enter Issue Here'})
        }

        labels = {
            'problem': _('')
        }

class ReportProblemFormLoggedInUser(forms.ModelForm):
    class Meta:
        model = ReportProblem
        fields = ('problem',)

        widgets = {
            'problem': forms.Textarea(attrs={'placeholder': 'Enter Issue Here'})
        }



    # name = forms.CharField()
    # email = forms.EmailField()
    # problem = forms.CharField(label='', 
    #                           widget=forms.Textarea)


# class ReportProblemFormLoggedInUser(forms.Form):
#     problem = forms.CharField(label='',
#                               widget=forms.Textarea)



class SearchForm(forms.Form):
    query = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder':'search for story'}),)