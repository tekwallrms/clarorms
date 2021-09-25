from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('idchart/<Rid>/', views.idchartdata.as_view()),
    path('datareport/', views.data_rep, name='datarep'),
    path('instreport/', views.data_rep, name='instrep'),
    path('biharsitedata/', views.custlist, name='rwsrj'),
    path('openIds/<Rid>/', views.openId, name='iddb'),
    path('search/', views.search, name='searchid'),
    path('mphome/', views.mp_home, name='mphome'),
    path('mpreport/', views.mp_rep, name='mprep'),
    path('mpcustomers/', views.mp_cust, name='mpcust'),
]