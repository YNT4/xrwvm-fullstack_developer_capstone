from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.registration, name='register'),
    path('session', views.get_session, name='session'),
    path(
    "dealers",
    views.get_dealerships,
    name="dealerships"),
    path(
    "dealer/<int:dealer_id>",
    views.get_dealer_by_id,
    name="dealer_by_id"),
    path(
    "get_cars",
    views.get_cars,
    name="get_cars"),
    path(
    'dealer/<int:dealer_id>/reviews',
    views.get_dealer_reviews,
    name='dealer_reviews'),
    path(
    "add_review",
    views.add_review,
    name="add_review"),
    path('csrf/', views.get_csrf_token, name='csrf'),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
