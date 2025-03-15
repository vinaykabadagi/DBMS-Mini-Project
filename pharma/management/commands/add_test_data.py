from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from pharma.models import Medicine, Brand, Batch, Customer, Sale, SaleItem
from datetime import timedelta, date
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Adds test data to the database'

    def handle(self, *args, **kwargs):
        # Create brands
        brands = [
            Brand.objects.create(name="Sun Pharma"),
            Brand.objects.create(name="Cipla"),
            Brand.objects.create(name="Dr. Reddy's"),
            Brand.objects.create(name="Mankind"),
        ]
        self.stdout.write(self.style.SUCCESS('Created brands'))

        # Create medicines
        medicines = []
        medicine_data = [
            ("Paracetamol", "Pain reliever and fever reducer", "10.50"),
            ("Amoxicillin", "Antibiotic", "15.75"),
            ("Omeprazole", "Acid reflux medication", "20.00"),
            ("Metformin", "Diabetes medication", "12.25"),
            ("Amlodipine", "Blood pressure medication", "18.50"),
            ("Cetirizine", "Antihistamine", "8.75"),
            ("Aspirin", "Pain reliever", "5.50"),
            ("Vitamin D3", "Supplement", "25.00"),
        ]

        for name, description, price in medicine_data:
            medicine = Medicine.objects.create(
                name=name,
                description=description,
                price=Decimal(price),
                brand=random.choice(brands)
            )
            medicines.append(medicine)
        self.stdout.write(self.style.SUCCESS('Created medicines'))

        # Create batches
        today = date.today()
        for medicine in medicines:
            # Create 2-3 batches per medicine
            for _ in range(random.randint(2, 3)):
                # Set unit price as 80% of medicine price (20% margin)
                unit_price = medicine.price * Decimal('0.8')
                Batch.objects.create(
                    medicine=medicine,
                    batch_number=f"B{random.randint(10000, 99999)}",
                    quantity=random.randint(50, 200),
                    manufacturing_date=today - timedelta(days=random.randint(30, 180)),
                    expiry_date=today + timedelta(days=random.randint(180, 720)),
                    unit_price=unit_price
                )
        self.stdout.write(self.style.SUCCESS('Created batches'))

        # Create customers
        customers = []
        customer_data = [
            ("John Doe", "1234567890", "john@example.com"),
            ("Jane Smith", "9876543210", "jane@example.com"),
            ("Bob Wilson", "5555555555", "bob@example.com"),
        ]

        for name, phone, email in customer_data:
            customer = Customer.objects.create(
                name=name,
                phone=phone,
                email=email,
                age=random.randint(25, 70),
                address=f"{random.randint(1, 999)} Main St, City"
            )
            customers.append(customer)
        self.stdout.write(self.style.SUCCESS('Created customers'))

        # Create sales
        for _ in range(20):  # Create 20 sales
            # Random date in the last 30 days
            sale_date = timezone.now() - timedelta(days=random.randint(0, 30))
            
            sale = Sale.objects.create(
                customer=random.choice(customers),
                created_at=sale_date,
                payment_method='cash',
                created_by=User.objects.get(username='admin')
            )

            # Add 1-4 items to each sale
            total_amount = Decimal('0')
            for _ in range(random.randint(1, 4)):
                batch = random.choice(Batch.objects.all())
                quantity = random.randint(1, 5)
                
                # Create sale item
                SaleItem.objects.create(
                    sale=sale,
                    batch=batch,
                    quantity=quantity,
                    unit_price=batch.unit_price
                )
                
                total_amount += quantity * batch.unit_price
                
                # Update batch quantity
                batch.quantity = max(0, batch.quantity - quantity)
                batch.save()

            sale.total_amount = total_amount
            sale.save()

        self.stdout.write(self.style.SUCCESS('Created sales')) 