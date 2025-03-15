from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, date
from .models import Medicine, Batch, Sale, SaleItem

@receiver(post_save, sender=Batch)
def check_stock_levels(sender, instance, created, **kwargs):
    """Send notification when stock is low or medicine is about to expire"""
    if instance.is_low_stock:
        # In a real application, you would send an actual email
        print(f"Low stock alert: {instance.medicine.name} has only {instance.quantity} units left")
    
    today = date.today()
    if instance.expiry_date and (instance.expiry_date - today).days <= 30:
        print(f"Expiry alert: {instance.medicine.name} batch {instance.batch_number} will expire on {instance.expiry_date}")

@receiver(post_save, sender=SaleItem)
def update_stock(sender, instance, created, **kwargs):
    """Update stock levels when a sale is made"""
    if created:
        batch = instance.batch
        batch.quantity = max(0, batch.quantity - instance.quantity)
        batch.save()

        # Update sale total
        sale = instance.sale
        sale.total_amount = sum(item.quantity * item.unit_price for item in sale.items.all())
        sale.save() 