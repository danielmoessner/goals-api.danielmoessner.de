from django import forms


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def prepare_value(self, value):
        value = super().prepare_value(value)
        if isinstance(value, str):
            return [value]
        return value
