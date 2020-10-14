from django import forms

from PDFApps.models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['Product_name','logo','description','quality','price','Sale_Date']
