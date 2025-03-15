from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    prescription_required = models.BooleanField(default=False)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.brand.name})"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Batch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=20, unique=True)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def is_expiring_soon(self):
        thirty_days_later = timezone.now().date() + timezone.timedelta(days=30)
        return self.expiry_date <= thirty_days_later and not self.is_expired

    @property
    def is_low_stock(self):
        return self.quantity <= 10

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number}"

class Prescription(models.Model):
    doctor_name = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='prescriptions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription by Dr. {self.doctor_name} ({self.date})"

class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale {self.id} - {self.customer.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.batch.medicine.name} x {self.quantity}"

class content(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class expiry(models.Model):
    date=models.DateField()

class quantity(models.Model):
    quant=models.PositiveIntegerField()
    expiry=models.ForeignKey(expiry,on_delete=models.PROTECT)
   
    

    