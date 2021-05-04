from django import forms 
   
# import GeeksModel from models.py 
from .models import customers ,Medicine
   
# create a ModelForm 
class CustomerForm(forms.ModelForm): 
    # specify the name of model to use 
    class Meta: 
        model = customers 
        fields = ['name','age','phone','address']
        name = forms.CharField()
        age=forms.IntegerField()
        phone=forms.IntegerField()
        address=forms.TextInput()
       