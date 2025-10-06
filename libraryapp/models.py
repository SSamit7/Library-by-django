from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    # isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    no_of_pages=models.IntegerField(max_length=5)
    price=models.IntegerField(max_length=5)
    semester=models.CharField(max_length=100)
    cover_image=models.ImageField(upload_to='media/')
    date_added=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"