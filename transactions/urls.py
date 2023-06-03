from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new/', views.SelectSupplierView.as_view(), name='select-supplier'),
    path('purchases/new/<int:pk>/', views.PurchaseCreateView.as_view(), name='new-purchase'),
    path('purchases/<pk>/delete/', views.PurchaseDeleteView.as_view(), name='delete-purchase'),

    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new/', views.SelectCostumerView.as_view(), name='select-costumer'),
    path('sales/new/<int:pk>/', views.SaleCreateView.as_view(), name='new-sale'),
    path('sale/<pk>/delete/', views.SaleDeleteView.as_view(), name='delete-sale'),


    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),

    path('agents/', views.AgentListView.as_view(), name='agent-list'),
    path('agents/new', views.AgentCreateView.as_view(), name='new-agent'),
    path('agents/<pk>/edit', views.AgentUpdateView.as_view(), name='edit-agents'),
    path('agents/<pk>/delete', views.AgentDeleteView.as_view(), name='delete-agents'),
    path('agents/<name>', views.AgentView.as_view(), name='agents'),


    path('costumer/', views.CostumerListView.as_view(), name='costumer-list'),
    path('costumer/new', views.CostumerCreateView.as_view(), name='new-costumer'),
    path('costumer/<pk>/edit', views.CostumerUpdateView.as_view(), name='edit-costumer'),
    path('costumer/<pk>/delete', views.CostumerDeleteView.as_view(), name='delete-costumer'),
    path('costumer/<name>', views.CostumerView.as_view(), name='costumer'),
]