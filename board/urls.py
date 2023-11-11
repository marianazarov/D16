from django.urls import path

from .views import AdsList, AdDetail, AdCreate, AdResponse, AdDelete, AdEdit, MyResponse, delete_responses, accept_responses


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),  # список постов
    path('<int:pk>/', AdDetail.as_view(), name='ad'),  #вывод одного поста)
    path('create', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/delete/', AdDelete.as_view(), name='ad_delete'),
    path('ad/<int:pk>/update/', AdEdit.as_view(), name='ad_update'),
    path('ads/<int:ad_id>/response/', AdResponse.as_view(), name='response'),
    path('my_responses', MyResponse.as_view(), name='my_responses'),
    path('delete-response/<int:pk>/', delete_responses, name='delete_response'),
    path('accept-response/<int:pk>/', accept_responses, name='accept_response'),

]