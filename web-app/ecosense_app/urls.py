from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('my_insights', views.ResearchInsightListView.as_view(), name='my-insights'),
    path('insight/<str:id>', views.ResearchInsightDetailView.as_view(), name="view-insight"),
    path('add_insight', views.ResearchInsightAddView.as_view(), name='add-insight'),
    path('edit_insight/<int:id>', views.ResearchInsightEditView.as_view(), name='edit-insight'),

    path('data/<str:slug>', views.data, name='data'),
    path('api/<str:slug>', views.api, name='api'),
    path('json_file/<str:slug>', views.json_file, name='json_file'),
    path('api_custom', views.api_custom, name='api_custom'),
    path('api_custom_data/<str:url>', views.api_custom_data, name='api_custom_data'),

    path('login', views.loginUser, name ='login'),
    path('register', views.registerUser, name ='register'),
    path('logout', views.logoutUser, name ='logout'),
]