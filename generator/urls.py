from django.contrib import admin
from django.urls import path, include
from generator import urls
from generator import views
from django.contrib.auth.views import  LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signin,name='signin'),
    path('index/', views.index,name='index'),
    path('upload_excel/', views.upload_excel,name='upload_excel'),
   	path('logout/', LogoutView.as_view(next_page = 'signin'), name = 'logout'),
    path('send_certificate_email/<int:id>', views.send_certificate_email,name='send_certificate_email'),
    path('list/', views.list,name='list'),
    path('student_index/', views.student_index,name='student_index'),
   
    
]
