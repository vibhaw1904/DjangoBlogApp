from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('create/', views.create_blog_post, name='create-blog-post'),
      path('posts/', views.blog_home, name='blog-posts'),
    path('my-posts/', views.my_post_view, name='my-posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete-post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit-post'),
 path('search-categories/', views.search_categories, name='search-categories'),
    path('search/',views.search_posts, name='search-posts'),
     path('choose-subscription/', views.choose_subscription, name='choose-subscription'),
    path('purchase-subscription/<int:plan_id>/', views.purchase_subscription, name='purchase-subscription'),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)