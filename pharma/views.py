from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from .models import Medicine,brands,customers,content,quantity,expiry
from django.db.models import Q
from .forms import CustomerForm 
from django.contrib import messages
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
    model = customers
    template_name = 'search_results2.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = customers.objects.filter(Q(name__icontains=query) | Q(phone__icontains=query))
        return object_list

def add_view(request): 
    if request.method == 'POST':
        fm = CustomerForm(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['age']
            ph = fm.cleaned_data['phone']
            ad = fm.cleaned_data['address']
            reg = customers(name=nm, age=em ,phone=ph, address=ad)
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
    item = customers.objects.get(id=item_id) 
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