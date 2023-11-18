from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import render, redirect
from .models import BlogPost,Subscription
from .forms import BlogPostForm
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .models import Category
from django.db.models import Q

from django.shortcuts import render

def choose_subscription(request):
    plans = Subscription.objects.all()
    return render(request, 'choose_subscription.html', {'plans': plans})

def purchase_subscription(request, plan_id):
     # Get the selected plan
    selected_plan = get_object_or_404(Subscription, pk=plan_id)

    # Assuming the user is authenticated, get the current user
    user = request.user

    # Check if the user already has an active subscription
    active_subscription = Subscription.objects.filter(user=user, is_active=True).first()

    if active_subscription:
        # If the user has an active subscription, mark it as expired
        active_subscription.is_active = False
        active_subscription.save()

    # Create a new subscription for the user with the selected plan
    new_subscription = Subscription.objects.create(
        user=user,
        plan=selected_plan,
        is_active=True  # Assuming the subscription is active upon purchase
        # Add any other necessary fields
    )

    # Perform actions or redirects based on successful subscription purchase
    # For example, redirect the user to a success page or dashboard
    return redirect('blog_home')

# def create_blog_post(request):
#     if request.method == 'POST':
#         user_subscription = Subscription.objects.get(user=request.user)
#         if user_subscription.plan == 'Basic':
#             today = timezone.now().date()
#             post_count_today = BlogPost.objects.filter(author=request.user, created_at__date=today).count()
#             if post_count_today >= user_subscription.posts_allowed:
#                 return HttpResponse("You have reached your daily post limit for Basic subscription.")
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('blog-home')
#     else:
#         form = BlogPostForm()
#     return render(request, 'my_create_blog_post.html', {'form': form})



def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        )
        return render(request, 'search_results.html', {'posts': posts})
    else:
        posts = BlogPost.objects.all()
    return render(request, 'search_results.html', {'posts': posts})

def search_categories(request):
    if 'category_query' in request.GET:
        query = request.GET['category_query']
        category_results = Category.objects.filter(author__username__icontains=query)
        return render(request, 'home.html', {'blog_posts': category_results})
    else:
        return render(request, 'blog_home.html', {'blog_posts': BlogPost.objects.all()})

def my_post_view(request):
    if request.user.is_authenticated:
        user_posts = BlogPost.objects.filter(author=request.user)
        return render(request, 'mypost.html', {'user_posts': user_posts})
    else:
        return redirect('login')

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        # Check if the logged-in user is the author of the post
        if request.user == post.author:
            post.delete()
            return redirect('my-posts')
        else:
            # Handle unauthorized delete attempt
            return HttpResponseForbidden("You are not allowed to delete this post.")
    return render(request, 'mypost.html')

def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my-posts')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog_home')  # Redirect to the homepage after creating the post
    else:
        form = BlogPostForm()
        return render(request, 'my_create_blog_post.html', { 'form': form })

def blog_home(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog_home.html', {'blog_posts': blog_posts})

def home(request):
    return render(request,'home.html',{})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home or any other page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blog-posts')  # Redirect to home or any other page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Redirect to home or any other page after logout
    return render(request, 'logout.html')


