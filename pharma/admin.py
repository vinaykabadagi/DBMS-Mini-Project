from django.contrib import admin
from .models import (
    Brand, Medicine, Customer, Batch,
    Prescription, Sale, SaleItem
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'brand', 'price', 'category', 'prescription_required')
    list_filter = ('brand', 'category', 'prescription_required')
    search_fields = ('name', 'generic_name')
    ordering = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')
    ordering = ('name',)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'medicine', 'quantity', 'unit_price', 
                   'manufacturing_date', 'expiry_date', 'is_expired', 'is_low_stock')
    list_filter = ('medicine__brand', 'expiry_date', 'quantity')
    search_fields = ('batch_number', 'medicine__name')
    date_hierarchy = 'expiry_date'
    ordering = ('expiry_date',)

    def is_expired(self, obj):
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'hospital', 'date')
    search_fields = ('doctor_name', 'hospital')
    date_hierarchy = 'date'
    ordering = ('-date',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    raw_id_fields = ('batch',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'payment_method', 
                   'created_by', 'created_at')
    list_filter = ('payment_method', 'created_at', 'created_by')
    search_fields = ('customer__name', 'customer__phone')
    date_hierarchy = 'created_at'
    inlines = [SaleItemInline]
    ordering = ('-created_at',)