from django import forms
from mailings.models import Notification


class FormStylesMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            elif field.widget.__class__.__name__ != 'DateTimeInput':
                field.widget.attrs['class'] = 'form-control'

class NotificationForm(FormStylesMixin, forms.ModelForm):
    class Meta:
        model = Notification
        fields = ('start_at', 'finish_at', 'period','client', 'message')

        widgets = {
            'start_at': forms.SelectDateWidget,
            'finish_at': forms.SelectDateWidget,
        }

        css = {
            'all': ('css/styles.css',)
        }
        js = ('js/script.js',)



