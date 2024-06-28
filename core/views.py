from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Order, User
from .forms import OrderForm, UserForm, LoginForm
from .serializers import OrderSerializer, UserSerializer

from rest_framework import viewsets

# Login View
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                csrf_token = get_token(request)  # Get the CSRF token
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username
                    },
                    'csrfToken': csrf_token  # Include CSRF token in the response
                })
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form data'}, status=400)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Logout View
@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'POST request required'}, status=400)

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

# Employee Management Views
@login_required
def manage_employees(request):
    if request.user.role != 'MANAGER':
        return redirect('home')
    employees = User.objects.filter(role='EMPLOYEE')
    return render(request, 'manage_employees.html', {'employees': employees})

@login_required
def add_employee(request):
    if request.user.role != 'MANAGER':
        return redirect('home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_employees')
    else:
        form = UserForm()
    return render(request, 'add_employee.html', {'form': form})

@login_required
def delete_employee(request, user_id):
    if request.user.role != 'MANAGER':
        return redirect('home')
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('manage_employees')

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
