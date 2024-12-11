from django.urls import path
from store import views


urlpatterns = [
     path('register/', views.User_Register.as_view(),name='register'),
     path('log/', views.User_Login.as_view(),name='signin'),
     path('vregister/', views.Vendorregister.as_view()),
     path('add/',views.Add_Category.as_view(),name='category'),
     path('add_product/',views.Add_Product.as_view(),name='product'),
     path('home/',views.Category_list.as_view(),name='category_list'),
     path('products/',views.Product_list.as_view(),name='product_list'),
     path('detail/<int:pk>',views.Product_detail.as_view(),name='productdet'),
     path('update/<int:pk>',views.Product_update.as_view()),
     path('category_detail/<int:pk>',views.Category_details.as_view(),name='categorydet'),
     path('cartadd/<int:pk>',views.Add_to_cart.as_view(),name='addtocart'),
     path('cartredir/<int:pk>',views.Cartredirect.as_view(),name='redir'),
     path('cartdlt/<int:pk>',views.Cart_delete.as_view()),
     path('order/<int:pk>',views.Orderview.as_view()),
     path('logout/',views.Logoutview.as_view()),
     path('olist/<int:pk>',views.Order_list.as_view()),


]