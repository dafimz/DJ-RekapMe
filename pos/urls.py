from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.login_page, name='login_page'),
    path('logout_page', views.logout_page, name='logout_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('billing/', views.billing, name='billing'),
    path('billing/order', views.order, name='order'),
    path('order_csv', views.order_csv, name='order_csv'),
]
