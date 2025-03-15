from django import forms
from .models import Medicine, Brand, Customer, Batch, Sale, SaleItem, Prescription

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class MedicineForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'generic_name', 'brand', 'description', 'price', 
                 'prescription_required', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BatchForm(BootstrapFormMixin, forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Batch
        fields = ['medicine', 'batch_number', 'quantity', 'unit_price', 
                 'manufacturing_date', 'expiry_date']
        widgets = {
            'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'age', 'phone', 'address', 'email']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class SaleForm(BootstrapFormMixin, forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={
            'class': 'select2-input',
            'data-placeholder': 'Search customer by name or phone'
        }),
        required=True,
        empty_label=None
    )
    
    class Meta:
        model = Sale
        fields = ['customer', 'payment_method', 'prescription']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Don't apply bootstrap class to customer field
        if 'customer' in self.fields:
            self.fields['customer'].widget.attrs['class'] = 'select2-input'
            # Only set initial value if we're editing an existing sale with a customer
            if self.instance and self.instance.pk and self.instance.customer_id:
                customer = self.instance.customer
                self.fields['customer'].initial = customer.id
                self.fields['customer'].widget.choices = [(customer.id, f"{customer.name} - {customer.phone}")]
            else:
                self.fields['customer'].initial = None
                self.fields['customer'].widget.choices = []

class SaleItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['batch', 'quantity', 'unit_price']

class PrescriptionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['doctor_name', 'hospital', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class MedicineSearchForm(BootstrapFormMixin, forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter name'})
    )
    category = forms.ChoiceField(
        choices=[],
        required=False,
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="All Brands"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct categories and create choices
        categories = Medicine.objects.values_list('category', flat=True).distinct().order_by('category')
        self.fields['category'].choices = [('', 'All Categories')] + [(c, c) for c in categories if c]
        
        # Update widget classes for consistent styling
        for field in self.fields.values():
            if isinstance(field.widget, (forms.Select, forms.NumberInput)):
                field.widget.attrs.update({'class': 'form-control'})
       