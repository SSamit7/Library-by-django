from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'copies_available']
    search_fields = ['title', 'author', ]

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'borrow_date', 'is_returned']
    list_filter = ['is_returned', 'borrow_date']