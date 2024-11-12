from rest_framework import serializers

from apps.notes.models import Note


class AddUserMixin:
    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "user" not in attrs:
            attrs["user"] = self.context["request"].user
        return attrs


class NoteSerializer(AddUserMixin, serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="note-detail")
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()

    class Meta:
        model = Note
        exclude = ["user"]


class NoteListSerializer(NoteSerializer):
    class Meta:
        model = Note
        exclude = ["user", "content"]
