from functools import lru_cache
from django.forms import Widget, Field, CharField, TextInput
from django.forms.widgets import Textarea
from django.forms.utils import flatatt
from django.forms.boundfield import BoundField
from django.utils.functional import cached_property
from django.utils.html import format_html


class LabelWidget(Widget):
    """
    Widget for LabelField
    """
    def render(self, name, value, attrs):
        attrs = self.build_attrs(attrs, name=name)
        if 'class' in attrs:
            attrs['class'] = attrs['class'].replace('form-control', '') # fix bootstrap lib
        if hasattr(self, 'initial'):
            value = self.initial
        return '<span %s>%s</span>' % (flatatt(attrs), value or '')


class LabelField(Field):
    """
    Simple field that shows only 'value' text
    Used with dynamic forms to show text between fields
    """
    widget = LabelWidget

    def __init__(self, *args, **kwargs):
        label = kwargs.setdefault('label', '')
        help_ = kwargs.pop('help_text', None)
        if not 'initial' in kwargs:
            kwargs['initial'] = help_ or label
        kwargs['required'] = False
        super().__init__(*args, **kwargs)

    def clean(self, value):
        self.widget.initial = self.initial
        return None


class EnchantedBoundField(BoundField):
    def css_classes(self, extra_classes=None):
        extra_css_classes = getattr(self.field, 'extra_css_classes', None)
        if extra_css_classes:
            if not extra_classes:
                extra_classes = []
            elif hasattr(extra_classes, 'split'):
                extra_classes = extra_classes.split()
            extra_classes.extend(extra_css_classes)
        return super().css_classes(extra_classes=extra_classes)

    def has_data(self):
        return self.data is not None

    @cached_property
    def display_data(self):
        data = self.data
        if hasattr(self.field, 'choices'):
            map_ = {k: v for k, v in self.field.choices}
            fmt = lambda a, b: "{}: {}".format(a, b) if b is not None and a != b else a
            if isinstance(data, list):
                data = [fmt(v, map_.get(v)) for v in data]
            else:
                data = fmt(data, map_.get(data))
        if isinstance(self.field.widget, Textarea):
            return format_html('<span class="textarea">{}</span>', data)

        return data

    @property
    def display_data_list(self):
        data = self.display_data
        if isinstance(data, list):
            return data
        return None


class BoundLabelField(EnchantedBoundField):
    auto_id = None


def _get_bound_field(self, form, field_name):
    if isinstance(self, LabelField):
        return BoundLabelField(form, self, field_name)
    return EnchantedBoundField(form, self, field_name)


@lru_cache(maxsize=None)
def get_enchanted_field(field_class, extra=None):
    member_dict = {}
    member_dict.update(extra or {})
    member_dict['get_bound_field'] = _get_bound_field
    return type(field_class.__name__, (field_class,), member_dict)

DummyField = get_enchanted_field.__wrapped__(CharField)
DUMMY_FIELD = DummyField(widget=TextInput(attrs={'readonly': True}))
