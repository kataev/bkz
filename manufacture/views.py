# Create your views here.
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from manufacture.forms import ManForm, AddFactory
from manufacture.models import Man

def man(request,id):
    """ Форма накладной """
    if id: doc = get_object_or_404(Man.objects.select_related(),pk=id)
    else: doc = None

    if request.method == 'POST':
        form = ManForm(request.POST,instance=doc,prefix='man',)
        add = AddFactory(request.POST,instance=doc,prefix='add')
        if form.is_valid() and add.is_valid():
            try:doc = form.save()
            except ValidationError,e: pass
            form.errors['__all__']=['test']
            add.save()
            return redirect(doc)
    else:

        form = ManForm(instance=doc,prefix='man')
        add = AddFactory(instance=doc,prefix='add')

    return render(request, 'doc.html',dict(doc=form,opers=[add]))