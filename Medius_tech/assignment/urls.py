from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name ="home-page"),
    path('upload/', views.upload_file, name='upload_file'),
    path('send-email/', views.send_summary_email, name='send_email')
]
