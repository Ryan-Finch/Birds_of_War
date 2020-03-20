from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('finches/', views.finches_index, name='index'),
    path('finches/<int:finch_id>/', views.finches_detail, name='detail'),
    path('finches/create/', views.FinchCreate.as_view(), name='finch_create'),
    path('finches/<int:pk>/update/', views.FinchUpdate.as_view(), name='finch_update'),
    path('finches/<int:pk>/delete/', views.FinchDelete.as_view(), name='finch_delete'),
    path('finces/<int:finch_id>/add_feeding/', views.add_sighting, name ='add_sighting'),

    path('armor/', views.ArmorList.as_view(), name='armor_list'),
    path('armor/create/', views.ArmorCreate.as_view(), name='armor_form'),
    path('armor/<int:pk>/', views.ArmorDetail.as_view(), name='armor_detail'),
    path('armor/<int:pk>/update/', views.ArmorUpdate.as_view(), name='armor_update'),
    path('armor/<int:pk>/delete/', views.ArmorDelete.as_view(), name='armor_delete')

]