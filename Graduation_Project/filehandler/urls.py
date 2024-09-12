from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file_view, name='upload_file'),  
    path('deploy/', views.deploy_contract_view, name='deploy_contract'),

]
