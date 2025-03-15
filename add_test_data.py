import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal
import pytz

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from pharma.models import Brand, Medicine, Customer, Batch, Sale, SaleItem

# Get or create test user
try:
    test_user = User.objects.get(username='testuser')
except User.DoesNotExist:
    test_user = User.objects.create_user('testuser', 'test@example.com', 'testpass')

# Clear existing sales data
Sale.objects.all().delete()

# Get existing data
customers = Customer.objects.all()
batches = Batch.objects.all()

if not customers.exists():
    # Create customers only if none exist
    customer_data = [
        ('John Doe', 35, '1234567890', '123 Main St', 'john@example.com'),
        ('Jane Smith', 45, '2345678901', '456 Oak Ave', 'jane@example.com'),
        ('Bob Johnson', 28, '3456789012', '789 Pine Rd', 'bob@example.com'),
        ('Alice Brown', 52, '4567890123', '321 Elm St', 'alice@example.com'),
    ]
    
    for name, age, phone, address, email in customer_data:
        Customer.objects.create(
            name=name,
            age=age,
            phone=phone,
            address=address,
            email=email
        )
    customers = Customer.objects.all()

if not batches.exists():
    # Create batches only if none exist
    medicines = Medicine.objects.all()
    if not medicines.exists():
        # Create medicines only if none exist
        brands = Brand.objects.all()
        if not brands.exists():
            # Create brands only if none exist
            brand_names = ['Sun Pharma', 'Cipla', 'Dr. Reddy\'s', 'Mankind']
            for name in brand_names:
                Brand.objects.create(
                    name=name,
                    description=f"Description for {name}",
                    website=f"https://www.{name.lower().replace(' ', '')}.com"
                )
            brands = Brand.objects.all()
        
        medicine_data = [
            ('Paracetamol', 'Acetaminophen', 'Pain Relief', False, Decimal('5.99')),
            ('Amoxicillin', 'Amoxicillin', 'Antibiotics', True, Decimal('15.99')),
            ('Omeprazole', 'Omeprazole', 'Gastric', False, Decimal('12.50')),
            ('Metformin', 'Metformin HCl', 'Diabetes', True, Decimal('8.99')),
            ('Amlodipine', 'Amlodipine Besylate', 'Blood Pressure', True, Decimal('10.99')),
        ]
        
        for name, generic, category, prescription_required, price in medicine_data:
            Medicine.objects.create(
                name=name,
                generic_name=generic,
                brand=random.choice(brands),
                description=f"Description for {name}",
                price=price,
                prescription_required=prescription_required,
                category=category
            )
        medicines = Medicine.objects.all()
    
    # Create batches
    today = timezone.now().date()
    for medicine in medicines:
        for i in range(2):  # 2 batches per medicine
            Batch.objects.create(
                medicine=medicine,
                batch_number=f"B{medicine.id}{i}{random.randint(1000,9999)}",
                quantity=random.randint(50, 200),
                unit_price=medicine.price * Decimal('0.7'),  # 70% of retail price
                manufacturing_date=today - timedelta(days=180),
                expiry_date=today + timedelta(days=550)
            )
    batches = Batch.objects.all()

# Reset all batch quantities
for batch in batches:
    batch.quantity = random.randint(100, 200)
    batch.save()

# Get the local timezone
local_tz = pytz.timezone('Asia/Kolkata')  # Using Indian timezone as an example

# Create sales for the past 30 days
now = timezone.now()
for days_ago in range(30):
    current_date = now.date() - timedelta(days=days_ago)
    
    # Create 1-3 sales per day
    for _ in range(random.randint(1, 3)):
        # Create a sale datetime between 9 AM and 5 PM
        naive_datetime = datetime.combine(
            current_date,
            datetime.min.time().replace(
                hour=random.randint(9, 17),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Make it timezone aware
        local_datetime = local_tz.localize(naive_datetime)
        utc_datetime = local_datetime.astimezone(pytz.UTC)
        
        sale = Sale.objects.create(
            customer=random.choice(customers),
            payment_method=random.choice(['cash', 'card', 'upi']),
            created_by=test_user,
            created_at=utc_datetime
        )
        
        # Add 1-3 items to each sale
        for _ in range(random.randint(1, 3)):
            batch = random.choice(batches)
            quantity = random.randint(1, 5)
            
            if batch.quantity >= quantity:
                SaleItem.objects.create(
                    sale=sale,
                    batch=batch,
                    quantity=quantity,
                    unit_price=batch.medicine.price
                )
                
                # Update batch quantity
                batch.quantity = max(0, batch.quantity - quantity)
                batch.save()
        
        # Update total amount
        sale.total_amount = sum(item.quantity * item.unit_price for item in sale.items.all())
        sale.save()

print("Test data has been added successfully!") 