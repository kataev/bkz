# -*- coding: utf-8 -*-
from django.shortcuts import render

def presentation(request):
    return render(request,'core/presentation.html')