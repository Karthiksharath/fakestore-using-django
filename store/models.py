from django.db import models
from django.contrib.auth.models import User


#pillow --> helps to handle graphical contents in django 

class Categorymodel(models.Model):

  category_name = models.CharField(max_length=100)
  category_image = models.ImageField(upload_to="images",null=True)

  def __str__(self):

    return self.category_name


class Productmodel(models.Model):

  product_name = models.CharField(max_length=100)
  product_image = models.ImageField(upload_to="images",null=True)
  product_description = models.TextField(null=True)
  product_price = models.IntegerField()
  prduct_stock = models.IntegerField()
  product_category = models.ForeignKey(Categorymodel,on_delete=models.CASCADE)



class Cartmodel(models.Model):

  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  product = models.ForeignKey(Productmodel,on_delete=models.CASCADE,null=True)
  total_price = models.DecimalField(decimal_places=2,max_digits=10,null=True)
  Date = models.DateTimeField(auto_now_add=True,null=True)


class Order(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  product = models.ForeignKey(Productmodel,on_delete=models.CASCADE,null=True)
  orderdate = models.DateTimeField(auto_now_add=True)
  Address = models.CharField(max_length=1000)