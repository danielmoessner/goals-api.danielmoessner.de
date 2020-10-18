from rest_framework import serializers
from apps.notes.models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='note-detail')
    id = serializers.ReadOnlyField()

    class Meta:
        model = Note
        exclude = ['user']
