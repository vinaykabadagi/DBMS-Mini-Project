from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F, DecimalField
from django.utils import timezone
from datetime import timedelta
from .models import Medicine, Brand, Customer, Batch, Sale, SaleItem, Prescription
from .forms import (
    MedicineForm, BatchForm, CustomerForm, SaleForm, 
    SaleItemForm, PrescriptionForm, MedicineSearchForm
)
from django.http import JsonResponse
from django.db.models.functions import Coalesce
from decimal import Decimal

# Create your views here.
class HomePageView(TemplateView):
    template_name='home.html'

class HomePageView2(TemplateView):
    template_name='home2.html'


class SearchResultsView(ListView):
    model = Medicine
    template_name = 'search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Medicine.objects.raw('SELECT * FROM pharma_medicine a,pharma_content d,pharma_medicine_content b where a.id=b.medicine_id and d.id=b.content_id and d.name = %s ',[query] )
        if object_list:
            return object_list
        else:
            object_list = Medicine.objects.raw('SELECT * FROM pharma_medicine where name = %s',[query])
            return object_list

class SearchResultsView2(ListView):
    model = Customer
    template_name = 'search_results2.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = Customer.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
        return object_list

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

def remove(request, item_id): 
    item = Medicine.objects.get(id=item_id) 
    item.delete() 
    messages.info(request, "Item removed !!!") 
    return redirect('home') 
def remove2(request, item_id): 
    item = Customer.objects.get(id=item_id) 
    item.delete() 
    messages.info(request, "Item removed !!!") 
    return redirect('home2') 

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
    template_name = 'pharma/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        # Sales analytics
        today_sales = Sale.objects.filter(
            created_at__date=today
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        context['today_sales'] = today_sales['total'] or 0

        monthly_sales = Sale.objects.filter(
            created_at__date__gte=thirty_days_ago
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        context['monthly_sales'] = monthly_sales

        # Get daily sales data for the chart
        daily_sales = []
        day_labels = []
        for i in range(7):
            date = today - timedelta(days=i)
            sales = Sale.objects.filter(created_at__date=date).aggregate(
                total=Sum('total_amount')
            )['total'] or 0
            daily_sales.insert(0, float(sales))
            day_labels.insert(0, date.strftime('%a'))
        
        import json
        context['sales_data'] = daily_sales
        context['day_labels'] = json.dumps(day_labels)

        # Inventory analytics
        # Get medicines with total quantity across all batches <= 10
        low_stock_medicines = Medicine.objects.annotate(
            total_stock=Sum('batch__quantity')
        ).filter(
            total_stock__lte=10
        ).select_related('brand')
        
        context['low_stock_items'] = low_stock_medicines
        context['low_stock_count'] = low_stock_medicines.count()

        expiring_soon = Batch.objects.filter(
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gte=today
        ).select_related('medicine')
        context['expiring_soon'] = expiring_soon
        context['expiring_soon_count'] = expiring_soon.count()

        # Top selling medicines
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
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.created_by = request.user
            sale.save()
            
            items_data = request.POST.get('items', '').split(';')
            total_amount = 0
            
            for item_data in items_data:
                if not item_data:
                    continue
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
            
            sale.total_amount = total_amount
            sale.save()
            
            messages.success(request, 'Sale completed successfully')
            return redirect('sale_detail', pk=sale.pk)
    else:
        form = SaleForm()
    
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
        reason = request.POST.get('reason')
        
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