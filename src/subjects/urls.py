from django.urls import path
from . import views


urlpatterns = [
    path('create-subject/', views.create_subject_view, name='create-subject'),
    path('assign-subject/<int:student_id>/', views.assign_subject_to_student, name='assign-subject')
   
]