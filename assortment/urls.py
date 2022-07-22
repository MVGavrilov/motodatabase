from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('motorcycle/<int:pk>/', views.AboutMotoView.as_view(), name='about_moto'),
    path('motorcycles/', views.MotorcyclesListView.as_view(), name='motorcycles_list'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('add_moto/', views.AddMotorcycleView.as_view(), name='add_moto_view'),
    path('add_user/', views.AddUserView.as_view(), name='add_user_view'),
    path('add_feature/<int:pk>/', views.AddFeatureView.as_view(), name='add_feature_view'),
    path('remove_feature/<int:pk>/', views.RemoveFeatureView.as_view(), name='remove_feature_view'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('add_model/', views.AddModelView.as_view(), name='add_model_view'),
    path('add_manufacturer/', views.AddManufacturerView.as_view(), name='add_manufacturer_view'),
    path('edit_moto/<int:pk>/', views.EditMotorcycleView.as_view(), name='edit_moto_view'),
    path('delete_moto/<int:pk>/', views.DeleteMotorcycleView.as_view(), name='delete_moto_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
