# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render, redirect

def main(request):
    return render(request,'lab.html')