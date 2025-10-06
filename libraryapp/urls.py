from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),
    path('borrowed/<int:pk>/', views.borrowed_book_detail, name='borrowed_book_detail'),
    path('borrowed/<int:pk>/return/', views.return_book, name='return_book'),
     path('profile/', views.profile_view, name='profile'),
]