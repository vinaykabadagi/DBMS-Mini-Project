from django.urls import path
from pharma import views
from .views import HomePageView, SearchResultsView, SearchResultsView2,HomePageView2,add_view,remove,update

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('search2/', SearchResultsView2.as_view(), name='search_results2'),
    path('home2/', HomePageView2.as_view(), name='home2'),
    path('', HomePageView.as_view(), name='home'),
    path('add/', views.add_view, name='add'),
    path('search/del/<item_id>', views.remove, name='del'),
    path('search2/del2/<item_id>', views.remove2, name='del2'),
    path('search/update/<item_id>', views.update, name='update'),
    
]