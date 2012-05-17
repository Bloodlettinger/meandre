# -*- coding: utf-8 -*-

from django import forms
from haystack.forms import SearchForm


class MainSearchForm(SearchForm):
    query = forms.CharField(required=False)

    def search(self):
        return super(MainSearchForm, self).search()
