from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import register, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry_page"),
    path("search/", views.search, name="search"),
    path("create-new-page/", views.create_new_page, name="create_new_page"),
    path("random/", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_page"),
    path('registration/register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile')
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)