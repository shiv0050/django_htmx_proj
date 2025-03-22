from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import time
from contacts.forms import ContactForm
from django.views.decorators.http import require_http_methods
# Create your views here.
@login_required
def index(request):
    contacts= request.user.contacts.all().order_by('-created_at')
    context = {'contacts':contacts,
               'form':ContactForm()}
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    query = request.GET.get('search','')
    time.sleep(1)
    contacts = request.user.contacts.filter(Q(name__icontains=query) | Q(email__icontains=query)).order_by('-created_at')
    context = {'contacts':contacts}
    return render(request, 'partials/contact-list.html', context)

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form=ContactForm(request.POST,request.FILES,initial={'user':request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        resp= render(request, 'partials/contact-row.html', {'contact':contact})
        resp["HX-Trigger"] = "contact-created"
        return resp
    else:
        resp= render(request, 'partials/add-contact-modal.html', {'form':form})
        resp['HX-Retarget']='#contact_modal'
        resp['HX-Reswap']='outerHTML'
        resp['HX-Trigger-After-Settle']='fail'
        return resp