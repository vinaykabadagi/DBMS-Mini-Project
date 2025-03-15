from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F, DecimalField, Max
from django.utils import timezone
from datetime import timedelta, datetime
import json
from .models import Medicine, Brand, Customer, Batch, Sale, SaleItem, Prescription
from .forms import (
    MedicineForm, BatchForm, CustomerForm, SaleForm, 
    SaleItemForm, PrescriptionForm, MedicineSearchForm
)
from django.http import JsonResponse
from django.db.models.functions import Coalesce
from decimal import Decimal
from django.db.models.deletion import ProtectedError
from django.utils.html import escape

# Create your views here.
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name='home.html'

class HomePageView2(LoginRequiredMixin, TemplateView):
    template_name='home2.html'


class SearchResultsView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return Medicine.objects.none()
            
        return Medicine.objects.filter(
            Q(name__iexact=query) |
            Q(content__name__iexact=query)
        ).distinct()

class SearchResultsView2(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'search_results2.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Customer.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
        return object_list

@login_required
def add_view(request): 
    if request.method == 'POST':
        fm = CustomerForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['age']
            ph = fm.cleaned_data['phone']
            ad = fm.cleaned_data['address']
            reg = Customer(name=nm, age=em ,phone=ph, address=ad)
            reg.save()
    else:
        fm = CustomerForm()
    return render(request,'add.html',{'form':fm})

@login_required
def remove(request, item_id): 
    item = Medicine.objects.get(id=item_id) 
    item.delete() 
    messages.info(request, "Item removed !!!") 
    return redirect('home') 

@login_required
def remove2(request, item_id): 
    item = Customer.objects.get(id=item_id) 
    item.delete() 
    messages.info(request, "Item removed !!!") 
    return redirect('home2') 

@login_required
def update(request, item_id):
    query = request.GET.get('q')
    item = quantity.objects.get(id=item_id)
    obj = get_object_or_404(quantity, id=item_id)
    if int(query)==0:
        item.delete() 
        messages.info(request, "Updated !!") 
        return redirect('home')
    obj.quant = query
    obj.save(update_fields=["quant"])
    messages.info(request, "Updated !!!") 
    return redirect('home') 

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view displaying key metrics and analytics:
    - Today's sales
    - Monthly sales
    - Daily sales chart (last 7 days)
    - Low stock alerts
    - Expiring inventory
    - Top selling medicines
    """
    template_name = 'pharma/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Calculate first and last day of current month for monthly metrics
        first_day = today.replace(day=1)
        if today.month == 12:
            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        # Get today's sales metrics
        today_sales = Sale.objects.filter(
            created_at__date=today
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        context['today_sales'] = today_sales['total'] or 0

        # Get monthly sales metrics
        monthly_sales = Sale.objects.filter(
            created_at__date__gte=first_day,
            created_at__date__lte=last_day
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        context['monthly_sales'] = monthly_sales

        # Calculate daily sales for the last 7 days for chart
        daily_sales = []
        day_labels = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            sales = Sale.objects.filter(created_at__date=date).aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            daily_sales.append(float(sales))
            day_labels.append(date.strftime('%Y-%m-%d'))
        
        context['sales_data'] = daily_sales
        context['day_labels'] = json.dumps(day_labels)

        # Get low stock alerts (items with quantity <= 10)
        low_stock_medicines = Medicine.objects.annotate(
            total_stock=Sum('batch__quantity')
        ).filter(
            total_stock__lte=10
        ).select_related('brand')
        
        context['low_stock_items'] = low_stock_medicines
        context['low_stock_count'] = low_stock_medicines.count()

        # Get items expiring in next 30 days
        expiring_soon = Batch.objects.filter(
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gte=today
        ).select_related('medicine')
        context['expiring_soon'] = expiring_soon
        context['expiring_soon_count'] = expiring_soon.count()

        # Get top 5 selling medicines
        context['top_medicines'] = Medicine.objects.annotate(
            total_sales=Sum('batch__saleitem__quantity')
        ).order_by('-total_sales')[:5]

        return context

class MedicineListView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'pharma/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MedicineSearchForm(self.request.GET)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = MedicineSearchForm(self.request.GET)
        
        if form.is_valid():
            # Apply filters independently
            if form.cleaned_data.get('search'):
                queryset = queryset.filter(
                    Q(name__icontains=form.cleaned_data['search']) |
                    Q(generic_name__icontains=form.cleaned_data['search'])
                )
            
            if form.cleaned_data.get('category'):
                queryset = queryset.filter(category=form.cleaned_data['category'])
            
            if form.cleaned_data.get('brand'):
                queryset = queryset.filter(brand=form.cleaned_data['brand'])
        
        # Always select_related brand to optimize queries
        return queryset.select_related('brand')

class MedicineDetailView(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = 'pharma/medicine_detail.html'
    context_object_name = 'medicine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = self.object.batch_set.all().order_by('expiry_date')
        context['sales_history'] = SaleItem.objects.filter(
            batch__medicine=self.object
        ).select_related('sale', 'batch')
        return context

class SaleDetailView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'pharma/sale_detail.html'
    context_object_name = 'sale'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('batch__medicine')
        return context

@login_required
def create_sale(request):
    """
    Handle creation of new sales:
    - Select customer
    - Add multiple medicine items
    - Calculate totals
    - Process payment
    - Update inventory
    """
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Create sale record
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            
            # Process sale items
            items_data = request.POST.get('items', '').split(';')
            total_amount = 0
            
            for item_data in items_data:
                if not item_data:
                    continue
                # Create sale items and update stock
                batch_id, quantity = item_data.split(',')
                batch = get_object_or_404(Batch, id=batch_id)
                quantity = int(quantity)
                
                if batch.quantity >= quantity:
                    item = SaleItem.objects.create(
                        sale=sale,
                        batch=batch,
                        quantity=quantity,
                        unit_price=batch.unit_price
                    )
                    total_amount += item.quantity * item.unit_price
                else:
                    messages.error(
                        request,
                        f'Insufficient stock for {batch.medicine.name}'
                    )
                    sale.delete()
                    return redirect('create_sale')
            
            # Update sale total
            sale.total_amount = total_amount
            sale.save()
            
            messages.success(request, 'Sale completed successfully')
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    
    # Get available batches for sale
    context = {
        'form': form,
        'batches': Batch.objects.filter(
            quantity__gt=0,
            expiry_date__gt=timezone.now().date()
        ).select_related('medicine')
    }
    return render(request, 'pharma/sale_form.html', context)

@login_required
def stock_adjustment(request, batch_id):
    batch = get_object_or_404(Batch, id=batch_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        reason = escape(request.POST.get('reason', ''))
        
        if new_quantity and reason:
            old_quantity = batch.quantity
            batch.quantity = new_quantity
            batch.save()
            
            messages.success(
                request,
                f'Stock adjusted from {old_quantity} to {new_quantity}'
            )
            return redirect('batch_detail', pk=batch_id)
    
    return render(request, 'pharma/stock_adjustment.html', {'batch': batch})

@login_required
def search_customers(request):
    """
    AJAX endpoint for customer search:
    - Used by Select2 dropdown in sale form
    - Search by name or phone
    - Return formatted results for dropdown
    """
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query)
        )[:10]
        data = [{
            'id': customer.id,
            'text': f"{customer.name} - {customer.phone}" if customer.phone else customer.name,
            'name': customer.name,
            'phone': customer.phone
        } for customer in customers]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required
def search_medicines(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(
        Q(name__icontains=query) | Q(generic_name__icontains=query)
    ).select_related('brand')[:10]
    
    data = [{
        'id': medicine.id,
        'text': f"{medicine.name} ({medicine.generic_name})",
        'brand': medicine.brand.name,
        'price': str(medicine.price)
    } for medicine in medicines]
    
    return JsonResponse(data, safe=False)

class CustomerListView(LoginRequiredMixin, ListView):
    """
    Display list of all customers with:
    - Search functionality
    - Purchase history
    - Total purchase amounts
    - Last purchase date
    """
    model = Customer
    template_name = 'pharma/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        # Apply search filters if query exists
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        
        # Add purchase statistics
        queryset = queryset.annotate(
            total_purchases=Count('sale'),
            total_amount=Sum('sale__total_amount'),
            last_purchase=Max('sale__created_at')
        )
        
        return queryset.order_by('-last_purchase')

class CustomerDetailView(LoginRequiredMixin, DetailView):
    """
    Show detailed customer information:
    - Personal details
    - Complete purchase history
    - Purchase statistics
    """
    model = Customer
    template_name = 'pharma/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get purchase history
        context['sales'] = self.object.sale_set.all().order_by('-created_at')
        
        # Calculate statistics
        stats = self.object.sale_set.aggregate(
            total_amount=Sum('total_amount'),
            total_purchases=Count('id')
        )
        context['stats'] = stats
        
        # Get recent purchases
        context['recent_purchases'] = self.object.sale_set.all().order_by('-created_at')[:5]
        
        return context

@login_required
def create_customer(request):
    """
    Handle customer creation with optional redirect:
    - Create new customer
    - Redirect back to sale creation if coming from there
    - Otherwise go to customer detail page
    """
    next_url = request.GET.get('next', None)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer added successfully')
            
            # Handle redirect after customer creation
            if next_url and 'create_sale' in next_url:
                return redirect(f'{next_url}?customer={customer.id}')
            return redirect('customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    return render(request, 'pharma/customer_form.html', {
        'form': form,
        'next_url': next_url
    })

@login_required
def delete_customer(request, pk):
    """
    Handle customer deletion:
    - Prevent deletion if customer has sales records
    - Show appropriate success/error messages
    """
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        try:
            name = escape(customer.name)  # Escape the name before using in message
            customer.delete()
            messages.success(request, f'Customer {name} has been deleted successfully')
        except ProtectedError:
            messages.error(request, f'Cannot delete customer {escape(customer.name)} because they have associated sales records')
        return redirect('customer_list')
    return redirect('customer_list')

@login_required
def sale_history(request):
    """
    Display complete sale history:
    - Show all sales with details
    - Include customer information
    - Show payment methods and totals
    Uses select_related and prefetch_related for optimal performance
    """
    sales = Sale.objects.all().select_related(
        'customer', 'created_by'
    ).prefetch_related(
        'items__batch__medicine'
    ).order_by('-created_at')
    
    return render(request, 'pharma/sale_history.html', {
        'sales': sales
    })

def handler404(request, exception):
    """Custom 404 error handler that doesn't expose paths"""
    return render(request, '404.html', status=404)

def handler500(request):
    """Custom 500 error handler that doesn't expose paths"""
    return render(request, '500.html', status=500) 