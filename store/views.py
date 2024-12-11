from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,ListView,UpdateView,DeleteView,DetailView
from store.forms import Userregisterform,Loginform,Categoryform,Productform,Orderform
from store.models import User,Categorymodel,Productmodel,Cartmodel,Order
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator


def sign_required(fn):

  def wrapper(request,*args,**kwargs):
    if not request.user.is_authenticated:
      return redirect('signin')
    else:
      return fn(request,*args,**kwargs)
  return wrapper


def My_login(fn):
  def wrapper(request,*args,**kwargs):
    id = kwargs.get("pk")
    data = Cartmodel.objects.get(id=id)
    if data.user!=request.user:
      return redirect('signin')
    else:
      return fn(request,*args,**kwargs)
  return wrapper



class User_Register(View):

  def get(self,request,*args,**kwargs):

    form = Userregisterform()
    return render(request,"register.html",{"form":form})
  
  def post(self,request,*args,**kwargs):

    form = Userregisterform(request.POST)
    if form.is_valid():
      u_name = form.cleaned_data.get("username")
      pwd = form.cleaned_data.get("password")
      email = form.cleaned_data.get("email")
      user = User.objects.create_user(username=u_name,password=pwd,email=email)
      # User.objects.create_user(**form.cleaned_data)

      subject = "welcome to Fakestore"
      message = f'Hii {user.username} Thank you for registering in fakestore'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [user.email,]
      send_mail(subject,message,email_from,recipient_list)
      
    form = Userregisterform()
    return render(request,"register.html",{"form":form})
  


class User_Login(View):
  def get(self,request,*args,**kwargs):

    form = Loginform()
    return render(request,"login.html",{"form":form})
  

  def post(self,request,*args,**kwargs):

    form = Loginform(request.POST)
    if form.is_valid():
      u_name = form.cleaned_data.get("username")
      pwd = form.cleaned_data.get("password")
      valid_user = authenticate(username=u_name,password=pwd)
      if valid_user:
        login(request,valid_user)
        print("valid user")
      form = Loginform()
      return render(request,"login.html",{"form":form})


#python manage.py create superuser (create superuser via terminal)
#superuser/admin
class Vendorregister(View):

  def get(self,request,*args,**kwargs):

    form = Userregisterform()
    return render(request,"register.html",{"form":form})
  
  def post(self,request,*args,**kwargs):

    form = Userregisterform(request.POST)
    if form.is_valid():
      User.objects.create_superuser(**form.cleaned_data)
    form = Userregisterform()
    return render(request,"register.html",{"form":form})
  
#electronics,beauty,groceries
class Add_Category(CreateView):

  model = Categorymodel
  form_class = Categoryform
  template_name = "category.html"
  success_url = reverse_lazy("register")


class Add_Product(CreateView):

  model = Productmodel
  form_class = Productform
  template_name = "product.html"
  success_url = reverse_lazy("register")


class Category_list(ListView):

  model = Categorymodel
  template_name = "home.html"
  context_object_name = "categories"


class Category_details(View):

  def get(self,request,*args,**kwargs):
    print(kwargs)
    id = kwargs.get("pk")
    data = Productmodel.objects.filter(product_category_id=id)
    return render(request,"productlist.html",{"products":data})


class Product_list(ListView):

  model = Productmodel
  template_name = "productlist.html"
  context_object_name = "products"


class Product_detail(DetailView):

  model = Productmodel
  template_name = "product_detail.html"
  context_object_name = "product_detail"



class Product_update(UpdateView):

  model = Productmodel
  template_name = "product.html"
  form_class = Productform
  success_url = reverse_lazy('category_list')


@method_decorator(sign_required,name='dispatch')
class Add_to_cart(View):

  def get(self,request,*args,**kwargs):

    id = kwargs.get("pk")
    data = Productmodel.objects.get(id=id)
    Cartmodel.objects.create(user=request.user,product=data)
    c_data = Cartmodel.objects.filter(user=request.user)
    price =  0
    for i in c_data:
      #more than 1 object in c_data so iterating
      if i.product and hasattr(i.product,'product_price'):
        #checking if the object have the field product and does it have the connecting field product_price.
        price+=i.product.product_price
    return render(request,"cart.html",{"c_data":c_data,"price":price})

@method_decorator(sign_required,name='dispatch')
class Cartredirect(View):

  def get(self,request,*args,**kwargs):
    c_data = Cartmodel.objects.filter(user=request.user)
    price =  0
    for i in c_data:
      if i.product and hasattr(i.product,'product_price'):
        price+=i.product.product_price
    return render(request,"cart.html",{"c_data":c_data,"price":price})



@method_decorator(sign_required,name='dispatch')
@method_decorator(My_login,name='dispatch')
class Cart_delete(View):

  def get(self,request,*args,**kwargs):

    id = kwargs.get("pk")
    Cartmodel.objects.get(id=id).delete()
    return redirect('redir')



@method_decorator(sign_required,name='dispatch')
@method_decorator(My_login,name='dispatch')
class Orderview(View):

  def get(self,request,*args,**kwargs):
    id = kwargs.get("pk")
    data = Productmodel.objects.get(id=id)
    form = Orderform()
    return render(request,"order.html",{"data":data,"form":form})


  def post(self,request,*args,**kwargs):
    
    id = kwargs.get("pk")
    data = Productmodel.objects.get(id=id)
    qs = Cartmodel.objects.create(user=request.user,product=data)
    form = Orderform(request.POST)
    if form.is_valid():
      Order.objects.create(user=request.user,product=data,**form.cleaned_data)
    Cartmodel.objects.get(id=qs.id).delete()
    return render(request,"order.html",{"data":data})


# @method_decorator(sign_required,name='dispatch')
class Order_list(View):

  def get(self,request,**kwargs):

    id = kwargs.get("pk")
    data = Order.objects.filter(user=request.user)
    return redirect(request,"orderlist.html",{"data":data})



class Logoutview(View):

  def get(self,request,**kwargs):
    logout(request)
    return redirect('signin')
  


