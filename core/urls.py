from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, UserViewSet, get_csrf_token, login_view, logout_view, create_order, edit_order, delete_order, order_list, manage_employees, add_employee, delete_employee, home

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create_order/', create_order, name='create_order'),
    path('order_list/', order_list, name='order_list'),
    path('edit_order/<int:order_id>/', edit_order, name='edit_order'),
    path('delete_order/<int:order_id>/', delete_order, name='delete_order'),
    path('manage_employees/', manage_employees, name='manage_employees'),
    path('add_employee/', add_employee, name='add_employee'),
    path('delete_employee/<int:user_id>/', delete_employee, name='delete_employee'),
    
    # API routes
    path('api/', include(router.urls)),
    path('api/csrf-token/', get_csrf_token, name='csrf-token'),
]
