from django.urls import path
from . import views
from .views import HomePageView, SearchResultsView, SearchResultsView2, HomePageView2

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Medicine Management
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    
    # Sales
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('sales/search-customers/', views.search_customers, name='search_customers'),
    
    # Inventory
    path('inventory/adjust/<int:batch_id>/', views.stock_adjustment, name='stock_adjustment'),
    
    # Search
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search2/', SearchResultsView2.as_view(), name='search_results2'),
    
    # Legacy paths (keeping for compatibility)
    path('home2/', HomePageView2.as_view(), name='home2'),
    path('add/', views.add_view, name='add'),
    path('search/del/<item_id>', views.remove, name='del'),
    path('search2/del2/<item_id>', views.remove2, name='del2'),
    path('search/update/<item_id>', views.update, name='update'),
]