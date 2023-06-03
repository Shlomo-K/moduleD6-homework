from django.urls import path
from .views import NewsList, PostDetail, SearchNews, PostCreateView, PostDeleteView, PostUpdateView, subscription 
 
 
urlpatterns = [
   
    
    path('', NewsList.as_view()), 
    path('search/', SearchNews.as_view()),
    path('add/', PostCreateView.as_view(), name='add_post'), 
    path('<int:pk>/', PostDetail.as_view(), name='detail_post'),
    path('subscription/', subscription, name='subscription'),
    path('add/<int:pk>', PostUpdateView.as_view(), name='edit_post'), 
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete_post'), 
    path('<int:pk>', PostDetail.as_view()),  

]