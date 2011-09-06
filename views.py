# -*- coding: utf-8 -*-
from django.shortcuts import render
from whs.bill.models import Bill


def main(request):
    return render(request, 'main.html')