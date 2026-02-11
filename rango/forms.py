from django import forms
from rango.models import Category, Page


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128,
        help_text="Please enter the category name."
    )

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128,
        help_text="Please enter the title of the page."
    )

    url = forms.CharField(
        max_length=200,
        help_text="Please enter the URL of the page."
    )

    views = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0
    )
    def clean_url(self):
        url = self.cleaned_data.get('url')

        if url and not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://' + url

        return url

    class Meta:
        model = Page
        exclude = ('category',)

