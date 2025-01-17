"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from authentication import views as authentication_views
from reviews import views as reviews_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication_views.home, name="home"),
    path("register/", authentication_views.register, name="register"),
    path("logout/", authentication_views.logout_view, name="logout"),
    path("login/", authentication_views.login_view, name="login"),
    path("feed/", reviews_views.feed, name="feed"),
    path("my_posts/", reviews_views.my_posts, name="my_posts"),
    path("my_posts/ticket_add/", reviews_views.ticket_create, name="ticket-add"),
    path("my_posts/review_add/", reviews_views.review_create, name="review-add"),
    path("my_posts/<int:id>/review_ticket/", reviews_views.review_ticket, name="review-ticket"),
    path("my_posts/<int:id>/review_update/", reviews_views.review_update, name="review-update"),
    path("my_posts/<int:id>/review_delete/", reviews_views.review_delete, name="review-delete"),
    path("my_posts/<int:id>/ticket_update/", reviews_views.ticket_update, name="ticket-update"),
    path("my_posts/<int:id>/ticket_delete/", reviews_views.ticket_delete, name="ticket-delete"),
    path("subscriptions/", reviews_views.subscriptions, name="subscriptions"),
    path("subscriptions/<int:id>/unfollow/", reviews_views.unfollow, name="unfollow"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
