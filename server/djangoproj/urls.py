from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views
from django.views.decorators.csrf import ensure_csrf_cookie
urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),

    path('', TemplateView.as_view(
        template_name="Home.html"
    ), name='home'),

    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path(
    'login',
    ensure_csrf_cookie(
        TemplateView.as_view(template_name="Login.html")
    ),
    name='login_page'),
    path(
    'register',
    ensure_csrf_cookie(
        TemplateView.as_view(template_name="Register.html")
    ),
    name='register_page'),
    path(
        'dealers',
        TemplateView.as_view(template_name="Dealers.html"),
        name='dealers_page'),
    path(
    'dealer/<int:dealer_id>',
    TemplateView.as_view(template_name="DealerDetails.html"),
    name='dealer_details_page'),
    path(
    'postreview/<int:dealer_id>',
    TemplateView.as_view(template_name="PostReview.html"),
    name='post_review_page'),

] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)