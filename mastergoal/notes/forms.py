from django import forms

from mastergoal.notes.models import Note

from tinymce.widgets import TinyMCE


# Goal
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)

    def __init__(self, user, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        self.instance.user = user
