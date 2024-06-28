from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, UserViewSet
from django.urls import path
from .views import get_csrf_token,login_view
from .views import logout_view

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/csrf-token/', get_csrf_token, name='csrf-token'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
]
