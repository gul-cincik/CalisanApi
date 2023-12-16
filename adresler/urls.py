from django.urls import path, include
from .views import AdreslerView, CreateAdresView, UpdateAdresView, DeleteAdresView
from .views import GetAllAdresView, GetAdresById, api_view_adres
from rest_framework.routers import DefaultRouter
from .views import AdreslerViewSet

router = DefaultRouter()
router.register(r'adresler_viewset', AdreslerViewSet, basename='adresler_viewset')

urlpatterns = [
    #APIViews
    path('AdresEkle/', AdreslerView.as_view()),
    path('AdresGuncelle/<int:pk>/', AdreslerView.as_view()),

    # generics
    path('CreateAdresView/', CreateAdresView.as_view()),
    path('UpdateAdresView/<int:pk>/', UpdateAdresView.as_view()),
    path('DeleteAdresView/<int:pk>/', DeleteAdresView.as_view()),
    path('GetAllAdresView/', GetAllAdresView.as_view()),
    path('GetAdresById/<int:pk>/', GetAdresById.as_view()),

    path('api_view_adres/', api_view_adres),
    path('api_view_adres/<int:pk>/', api_view_adres),

    
    path('', include(router.urls)),
]