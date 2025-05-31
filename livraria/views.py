from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddBookForm
from .models import Book

def home(request):
    books = Book.objects.all()
    if request.method == "POST":
        username = request.POST['usuario']
        password = request.POST['senha']
        user = authenticate(
            request,
            username=username,
            password=password  
        )
        if user is not None:
            login(request, user)
            messages.success(
                request,
                "Login realizado!"
            )
            return redirect('home')
        else:
            messages.error(
                request,
                "Erro na autenticação, TENTE NOVAMENTE!"
            )
            return redirect('home')
    else:
        return render(request, 'home.html', {'books': books})


def logout_user(request):
    logout(request)
    messages.success(
        request,
        "Logout com sucesso!!"
    )
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(
                username=username,
                password=password
            )
            login(request, user)
            messages.success(
                request,
                "Fez login com o novo usuário!"
            )
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def book_detail(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        return render(request, 'book.html', {'book': book})
    else:
        messages.error(request, 'Necessário fazer login!!')
        return redirect('home')
    

def book_delete(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        book.delete()
        messages.success(request, 'Livro excluído com sucesso!!')
        return redirect('home')
    else:
        messages.error(request, 'Necessário fazer login')
        return redirect('home')
    

def book_add(request):
    form = AddBookForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Livro cadastrado com sucesso!!")
                return redirect('home')
        return render(request, 'add_book.html', {'form': form})
    else:
        messages.error(request, "Necessário realizar login!!")
        return redirect('home')
    

def book_update(request, id):
    if request.user.is_authenticated:
        book = Book.objects.get(id=id)
        form = AddBookForm(request.POST or None, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Atualizado com sucesso!!")
            return redirect('home')
        return render(request, 'update_book.html', {'form': form})
    else:
        messages.error(request, "Necessário realizar login!!")
        return redirect('home')



















