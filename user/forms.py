# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='Upload json file only',
        widget=forms.FileInput(attrs={'accept':'application/json'})
    )
