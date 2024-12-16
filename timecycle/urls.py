from django.urls import path 
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new-cycle', views.NewTimeCycleView.as_view(), name='new-cycle'),
    path('cycles/', views.ViewCyclesView.as_view(), name='view-cycles'),
    path('activities/', views.ViewActivitiesView.as_view(), name='view-activities'),
    path('new-activity', views.NewActivityView.as_view(), name='new-activity'),
    path('edit-cycle/<int:pk>/', views.EditCycleView.as_view(), name='edit-cycle'),
    path('edit-activity/<int:pk>/', views.EditActivityView.as_view(), name='edit-activity'),
    path('success', views.SuccessView.as_view(), name='success'),
]