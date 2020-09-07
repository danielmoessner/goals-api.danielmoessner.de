from django import forms


class DeleteForm(forms.Form):
    pk = forms.IntegerField(min_value=0)

    class Meta:
        fields = (
            "pk"
        )
