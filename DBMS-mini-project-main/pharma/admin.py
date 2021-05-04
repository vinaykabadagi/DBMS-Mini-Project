from django.contrib import admin

# Register your models here.
from .models import Medicine,brands,content,customers,quantity,expiry

#from .models import expiry
@admin.register(Medicine,brands,content,quantity,expiry)
class madmin(admin.ModelAdmin):
    pass

@admin.register(customers)
class cadmin(admin.ModelAdmin):
    list_display=['name','phone','address']