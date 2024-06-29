from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets

from .models import Order, User
from .forms import OrderForm, UserForm
from .serializers import OrderSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
def home(request):
    if request.user.is_authenticated:
        return redirect('order_list')
    else:
        return redirect('login')

# Login View
@csrf_exempt
def login_view(request):
    print("Login view called")
    if request.method == 'POST':
        print("POST request received")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            print(f"Authenticating user: {user.username}")
            login(request, user)
            print(f"User {user.username} logged in successfully")
            return redirect('order_list')  # Redirect to 'order_list' view
        else:
            print(f"Invalid credentials: {form.errors}")
            return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        print("GET request received, rendering login form")
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('login')

# Order Views
@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'edit_order.html', {'form': form, 'order': order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'delete_order.html', {'order': order})

# Employee Management Views
@login_required
def manage_employees(request):
    if request.user.role != 'MANAGER':
        return redirect('order_list')
    employees = User.objects.exclude(id=request.user.id) 
    # employees = User.objects.filter(role='EMPLOYEE')
    return render(request, 'manage_employees.html', {'employees': employees})

@login_required
def add_employee(request):
    if request.user.role != 'MANAGER':
        return redirect('order_list')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('manage_employees')
    else:
        form = UserForm()
    return render(request, 'add_employee.html', {'form': form})

@login_required
def delete_employee(request, user_id):
    if request.user.role != 'MANAGER':
        return redirect('order_list')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_employees')
    return render(request, 'delete_employee.html', {'user': user})

# CSRF Token View
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# ViewSets
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
