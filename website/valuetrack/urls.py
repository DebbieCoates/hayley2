from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('suppliers/', views.suppliers, name='suppliers'),
    path('solutions/', views.solutions, name='solutions'),
    path('problems/', views.problems, name='problems'),
    path('supplier/<int:supplier_id>/', views.supplier_detail, name='supplier_detail'),
    path('solution/<int:solution_id>/', views.solution_detail, name='solution_detail'),

]