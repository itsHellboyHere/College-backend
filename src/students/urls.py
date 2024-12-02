from django.urls import path
from . import views

urlpatterns = [
    path('create-profile/', views.student_detail_create_view, name='create-profile'),
    path('view/', views.student_list_view,name='student-detail'),
    path('update/', views.student_detail_update_view,name='student-update'),
    path('profile-pic/update/',views.student_profile_pic_update_view,name='profile-pic'),
    path('subjects/',views.student_subject_view,name='subjects'),
    path('profile-pic/', views.get_profile_pic_view, name='student-profile-pic-url'),

]
