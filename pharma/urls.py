from django.urls import path
from . import views
from .views import HomePageView, SearchResultsView, SearchResultsView2, HomePageView2

# URL patterns for the pharmacy management system
urlpatterns = [
    # Dashboard - Main entry point of the application
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Medicine Management URLs
    # Handles medicine listing, details, and related operations
    path('medicines/', views.MedicineListView.as_view(), name='medicine_list'),
    path('medicines/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine_detail'),
    
    # Customer Management URLs
    # Handles customer CRUD operations and viewing
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/add/', views.create_customer, name='create_customer'),
    path('customers/<int:pk>/delete/', views.delete_customer, name='delete_customer'),
    
    # Sales Management URLs
    # Handles sales creation, history, and customer search during sales
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('sales/search-customers/', views.search_customers, name='search_customers'),
    path('sales/history/', views.sale_history, name='sale_history'),
    
    # Inventory Management URLs
    # Handles stock adjustments and inventory operations
    path('inventory/adjust/<int:batch_id>/', views.stock_adjustment, name='stock_adjustment'),
    
    # Search URLs
    # Handles medicine and customer search functionality
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search2/', SearchResultsView2.as_view(), name='search_results2'),
    
    # Legacy URLs
    # Maintained for backward compatibility - consider deprecating
    path('home2/', HomePageView2.as_view(), name='home2'),
    path('add/', views.add_view, name='add'),
    path('search/del/<item_id>', views.remove, name='del'),
    path('search2/del2/<item_id>', views.remove2, name='del2'),
    path('search/update/<item_id>', views.update, name='update'),
]