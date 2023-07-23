from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

import app.views as views

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'),
  path('chart/', views.ChartView.as_view(), name='chart_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)