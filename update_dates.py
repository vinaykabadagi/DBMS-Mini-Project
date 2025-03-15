import os
import django
import random
from datetime import datetime, timedelta
import pytz

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy.settings')
django.setup()

from django.utils import timezone
from pharma.models import Medicine, Customer, Sale, Batch

# Get the local timezone
local_tz = pytz.timezone('Asia/Kolkata')  # Using Indian timezone as an example

# Update some medicine created dates (last 30 days)
medicines = Medicine.objects.all()
for medicine in medicines[:3]:  # Update first 3 medicines
    days_ago = random.randint(15, 30)
    new_date = timezone.now() - timedelta(days=days_ago)
    Medicine.objects.filter(id=medicine.id).update(
        created_at=new_date,
        updated_at=new_date
    )

# Update some customer created dates (last 60 days)
customers = Customer.objects.all()
for customer in customers[:2]:  # Update first 2 customers
    days_ago = random.randint(30, 60)
    new_date = timezone.now() - timedelta(days=days_ago)
    Customer.objects.filter(id=customer.id).update(created_at=new_date)

# Update some batch created dates (last 90 days)
batches = Batch.objects.all()
for batch in batches[:5]:  # Update first 5 batches
    days_ago = random.randint(60, 90)
    new_date = timezone.now() - timedelta(days=days_ago)
    Batch.objects.filter(id=batch.id).update(created_at=new_date)

# Get all sales
sales = Sale.objects.all()
now = timezone.now()

# Update each sale with a random date in the past 30 days
for sale in sales:
    days_ago = random.randint(0, 29)
    current_date = now.date() - timedelta(days=days_ago)
    
    # Create a random time between 9 AM and 5 PM
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
    
    # Update the sale date
    sale.created_at = utc_datetime
    sale.save()

print("Successfully updated dates for:")
print(f"- {len(medicines[:3])} medicines (15-30 days ago)")
print(f"- {len(customers[:2])} customers (30-60 days ago)")
print(f"- {len(batches[:5])} batches (60-90 days ago)")
print(f"- {len(sales[:10])} sales (15-30 days ago)") 