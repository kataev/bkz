# -*- coding: utf-8 -*-
from django import forms

from bkz.cpu.models import Position, Device


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device

