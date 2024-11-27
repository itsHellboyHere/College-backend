from django.urls import path
from . import views

urlpatterns=[
    path('create-student/',views.faculty_create_student_view,name='index'),
    path('view/',views.list_view_all_student),
    path('student/<int:id>/', views.get_single_student_view, name='single-student'),
]
