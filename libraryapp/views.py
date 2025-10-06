from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Book, BorrowRecord
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

#views (keep these as they are)


def profile_view(request):
    return render(request, 'libraryapp/profile.html')



def book_list(request):
    books = Book.objects.all()
    return render(request, 'libraryapp/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'libraryapp/book_details.html', {'book': book})

# Updated borrow_book view
@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # Check if user already has this book borrowed
    already_borrowed = BorrowRecord.objects.filter(
        book=book, 
        user=request.user, 
        is_returned=False
    ).exists()
    
    if already_borrowed:
        messages.warning(request, 'You have already borrowed this book!')
        return redirect('book_detail', pk=pk)
    
    if book.copies_available > 0:
        BorrowRecord.objects.create(book=book, user=request.user)
        book.copies_available -= 1
        book.save()
        messages.success(request, f'You have successfully borrowed "{book.title}"')
        return redirect('borrowed_books')  # Redirect to borrowed books page
    else:
        messages.error(request, 'Sorry, this book is currently unavailable')
        return redirect('book_detail', pk=pk)

# New view for borrowed books list
@login_required
def borrowed_books(request):
    borrowed = BorrowRecord.objects.filter(
        user=request.user, 
        is_returned=False
    ).select_related('book').order_by('-borrow_date')
    return render(request, 'libraryapp/borrowed_books.html', {'borrowed_books': borrowed})

# New view for borrowed book detail
@login_required
def borrowed_book_detail(request, pk):
    borrow_record = get_object_or_404(
        BorrowRecord, 
        pk=pk, 
        user=request.user, 
        is_returned=False
    )
    
    # Calculate due date (14 days from borrow date)
    due_date = borrow_record.borrow_date + timedelta(days=14)
    days_borrowed = (timezone.now().date() - borrow_record.borrow_date).days
    is_overdue = timezone.now().date() > due_date
    
    context = {
        'borrow_record': borrow_record,
        'due_date': due_date,
        'days_borrowed': days_borrowed,
        'is_overdue': is_overdue,
    }
    return render(request, 'libraryapp/borrowed_book_detail.html', context)

# New view for returning books
@login_required
def return_book(request, pk):
    borrow_record = get_object_or_404(
        BorrowRecord, 
        pk=pk, 
        user=request.user, 
        is_returned=False
    )
    
    # Mark as returned
    borrow_record.is_returned = True
    borrow_record.return_date = timezone.now().date()
    borrow_record.save()
    
    # Increase available copies
    book = borrow_record.book
    book.copies_available += 1
    book.save()
    
    messages.success(request, f'You have successfully returned "{book.title}"')
    return redirect('borrowed_books')

# Authentication views (keep these as they are)
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to the library.')
            return redirect('book_list')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserCreationForm()
    return render(request, 'libraryapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('book_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'libraryapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('book_list')

@login_required
def profile_view(request):
    borrowed_books = BorrowRecord.objects.filter(user=request.user, is_returned=False)
    history = BorrowRecord.objects.filter(user=request.user, is_returned=True).order_by('-return_date')
    return render(request, 'libraryapp/profile.html', {
        'borrowed_books': borrowed_books,
        'history': history
    })