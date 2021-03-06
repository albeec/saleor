import json
from typing import Optional

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django_prices.forms import MoneyField
from draftjs_sanitizer import SafeJSONEncoder
from prices import Money


def set_initial_money(instance: models.Model, field_name: str, field: MoneyField):
    money_field = getattr(instance, field_name)  # type: Optional[Money]
    if money_field is None:
        value = [None, settings.DEFAULT_CURRENCY]
    else:
        value = [money_field.amount, money_field.currency]
        if not money_field.currency:
            value[1] = settings.DEFAULT_CURRENCY

    field.initial = value


class MoneyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._money_fields = {
            field_name: field
            for field_name, field in self.fields.items()
            if isinstance(field, MoneyField)
        }

        for field_name, field in self._money_fields.items():
            set_initial_money(self.instance, field_name, field)

    def save(self, commit=True):
        for field_name, field in self._money_fields.items():
            value = self.cleaned_data[field_name]  # type: Money
            if value is None:
                # Preserve the currency value
                setattr(self.instance, f"{field_name}_amount", None)
            else:
                setattr(self.instance, field_name, value)

        return super(MoneyModelForm, self).save(commit=commit)


class ModelChoiceOrCreationField(forms.ModelChoiceField):
    """ModelChoiceField with the ability to create new choices.

    This field allows to select values from a queryset, but it also accepts
    new values that can be used to create new model choices.
    """

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or "pk"
            obj = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            return value
        else:
            return obj


class OrderedModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def clean(self, value):
        qs = super().clean(value)
        keys = list(map(int, value))
        return sorted(qs, key=lambda v: keys.index(v.pk))


class AjaxSelect2ChoiceField(forms.ChoiceField):
    """An AJAX-based choice field using Select2.

    fetch_data_url - specifies url, from which select2 will fetch data
    initial - initial object
    """

    def __init__(self, fetch_data_url="", initial=None, min_input=2, *args, **kwargs):
        self.queryset = kwargs.pop("queryset", None)
        super().__init__(*args, **kwargs)
        self.widget.attrs["class"] = "enable-ajax-select2"
        self.widget.attrs["data-url"] = fetch_data_url
        self.widget.attrs["data-min-input"] = min_input
        if initial:
            self.set_initial(initial)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            value = self.queryset.get(pk=value)
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise forms.ValidationError(
                self.error_messages["invalid_choice"], code="invalid_choice"
            )
        return value

    def valid_value(self, value):
        forms.Field.validate(self, value)
        return True

    def set_initial(self, obj, obj_id=None, label=None):
        """Set initially selected objects on field's widget."""
        selected = {
            "id": obj_id if obj_id is not None else obj.pk,
            "text": label if label else str(obj),
        }
        self.widget.attrs["data-initial"] = json.dumps(selected, cls=SafeJSONEncoder)

    def set_fetch_data_url(self, fetch_data_url):
        self.widget.attrs["data-url"] = fetch_data_url


class AjaxSelect2CombinedChoiceField(AjaxSelect2ChoiceField):
    """An AJAX-based choice field using Select2 for multiple querysets.

    Value passed to a field is of format '<obj.id>_<obj.__class__.__name__>',
    e. g. '17_Collection' for Collection object with id 17.

    fetch_data_url - specifies url, from which select2 will fetch data
    initial - initial object
    """

    def __init__(self, *args, **kwargs):
        self.querysets = kwargs.pop("querysets")
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None

        pk, model_name = value.split("_")
        queryset = next(
            (qs for qs in self.querysets if qs.model.__name__ == model_name), None
        )

        value = queryset.filter(pk=pk).first() if queryset else None

        if not value:
            raise forms.ValidationError(
                self.error_messages["invalid_choice"], code="invalid_choice"
            )
        return value


class AjaxSelect2MultipleChoiceField(forms.MultipleChoiceField):
    """An AJAX-base multiple choice field using Select2.

    fetch_data_url - specifies url, from which select2 will fetch data
    initial - list of initial objects
    """

    def __init__(self, fetch_data_url="", initial=[], min_input=2, *args, **kwargs):
        self.queryset = kwargs.pop("queryset")
        super().__init__(*args, **kwargs)
        self.widget.attrs["class"] = "enable-ajax-select2"
        self.widget.attrs["data-url"] = fetch_data_url
        self.widget.attrs["data-min-input"] = min_input
        if initial:
            self.set_initial(initial)
        self.widget.attrs["multiple"] = True

    def to_python(self, value):
        # Allow to set empty field
        if value == []:
            return value
        if value in self.empty_values:
            return None
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(
                self.error_messages["invalid_list"], code="invalid_list"
            )
        for choice in value:
            try:
                self.queryset.get(pk=choice)
            except (ValueError, TypeError, self.queryset.model.DoesNotExist):
                raise forms.ValidationError(
                    self.error_messages["invalid_choice"], code="invalid_choice"
                )
        return [str(val) for val in value]

    def valid_value(self, value):
        forms.Field.validate(self, value)
        return True

    def set_initial(self, objects):
        """Set initially selected objects on field's widget."""
        selected = [{"id": obj.pk, "text": str(obj)} for obj in objects]
        self.widget.attrs["data-initial"] = json.dumps(selected, cls=SafeJSONEncoder)


class PermissionMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Permission multiple choice field with label override."""

    def label_from_instance(self, obj):
        return obj.name


class ConfigBooleanField(forms.BooleanField):
    def to_python(self, value):
        return {"name": self.label, "value": super().to_python(value)}


class ConfigCharField(forms.CharField):
    def clean(self, value):
        parsed_value = super().clean(value)
        return {"name": self.label, "value": parsed_value}


class ConfigPasswordField(ConfigCharField):
    def __init__(self, *args, **kwargs):
        self.widget = forms.PasswordInput(render_value=True)
        super().__init__(*args, **kwargs)
