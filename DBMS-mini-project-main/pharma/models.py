from django.db import models

# Create your models here.
class brands(models.Model):
    name=models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name


class Medicine(models.Model):
    name=models.CharField(max_length=100,unique=True)
    content=models.ManyToManyField('content')
    quantity=models.ManyToManyField('quantity')
    brands=models.ForeignKey(brands,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class customers(models.Model):
    name=models.CharField(max_length=20)
    age=models.PositiveIntegerField()
    phone=models.PositiveIntegerField(unique=True)
    address=models.CharField(max_length=100)
    medicine=models.ManyToManyField('medicine')
    def __str__(self):
        return self.name

class content(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class expiry(models.Model):
    date=models.DateField()

class quantity(models.Model):
    quant=models.PositiveIntegerField()
    expiry=models.ForeignKey(expiry,on_delete=models.PROTECT)
   
    

    