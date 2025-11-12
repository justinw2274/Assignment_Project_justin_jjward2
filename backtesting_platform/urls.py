from django.contrib import admin
from django.urls import path, include
from paper_trader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('', include('paper_trader.urls')),
]
