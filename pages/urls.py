from django.urls import path
from . import views 

app_name = 'pages'

urlpatterns = [
    path('', views.home_page_view, name='home'), 
    path('about/', views.about_page_view, name='about'),
    path('report-problem/', views.report_problem, name='report-problem'),
    path('search/', views.search_page, name='search')
]