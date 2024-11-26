from django.urls import path

from . import views

urlpatterns=[
   path('login/',views.login_create_view),
   path('register/',views.register_create_view),
   path('register/faculty/',views.register_faculty_view),
   path('logout/',views.logout_view),
]