from django import forms

from uploads.core.models import Json, Yaml, Name

class JsonForm(forms.ModelForm):
    class Meta:
        model = Json
        fields = ('document', )

class YamlForm(forms.ModelForm):
    class Meta:
        model = Yaml
        fields = ('document', )

class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ('your_name', )

