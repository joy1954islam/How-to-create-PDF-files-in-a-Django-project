from django.contrib import messages
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import ListView,CreateView

from PDFApps.forms import CustomerForm
from PDFApps.models import Customer


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class PDFLISTVIEW(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return Customer.objects.all().order_by('Sale_Date')


def render_pdf_view(request,*args,**kwargs):
    pk = kwargs.get('pk')
    customer = get_object_or_404(Customer,pk=pk)
    template_path = 'user_printer.html'
    context = {'customer': customer}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class PDFCreate(CreateView):
    form_class = CustomerForm
    template_name = 'pdf_create.html'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request,messages.INFO,'BARCODE SAVE SUCCESSFULLY')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('create')