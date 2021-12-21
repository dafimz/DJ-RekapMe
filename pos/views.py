from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Customer, OrderItem, Order
import csv

def order_csv(request):
    response = HttpResponse(content_type='text/csv')
    response ['Content-Disposition'] = 'attachment; filename="order.csv"'
    
    writer = csv.writer(response)

    orders = Order.objects.all()
    writer.writerow(['Cashier Name','Total_Price', 'Status', 'Time'])

    for order in orders:
        writer.writerow([order.customer, order.total_price, order.success, order.timestamp])

    return response

def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method =="POST":
        username_login=request.POST['username']
        password_login=request.POST['password']

        user = authenticate(request, username=username_login, password=password_login)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request, ("Login Gagal!!!"))
            return redirect('login_page')

    return render(request, 'login_page.html')

def logout_page(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!, See Ya..."))
    return redirect('login_page')



def dashboard(request):
    return render(request, 'dashboard.html')

def billing(request):
    if request.method == 'GET':
        return render(request, 'billing.html')
    else:
        cid = request.POST.get('customerID', None)
        customer = Customer.objects.get(pk=cid)
        products = list(Product.objects.all())
        # context = { 'cust' : customer.identity,
        #             'name' : customer.name,
        #             'balance' : customer.balance,
        #             'products': products, }
        return render(request, 'billing_details.html', {'customer': customer, 'products': products})

def order(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('data', None))
        if data is None:
            raise AttributeError
        print(data)
        customer = Customer.objects.get(pk=data['customer_id'])
        order = Order.objects.create(customer=customer,
                                    total_price=data['total_price'],
                                    success=False)
        for product_id in data['product_ids']:
            OrderItem(product=Product.objects.get(pk=product_id), order=order).save()
        if data['total_price'] <= customer.balance:
            customer.balance -= int(data['total_price'])
            customer.save()
            order.success = True
        order.save()
        return render(request, 'order.html', {'success' : order.success})
