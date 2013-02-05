from django.shortcuts import render

def server_error(request,template_name='500.html'):
    return render(request,'500.html')
