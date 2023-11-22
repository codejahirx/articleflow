from django.urls import path
from blogapp import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:catslug>/', views.category, name='category'),
    path('tag/<slug:tagslug>/', views.tag_posts, name='tag_posts'),
    path('about-us', views.about_page, name='about'),
    path('contact-us', views.contact_page, name='contact'),
    path('search', views.search, name='searchbar'),

]
