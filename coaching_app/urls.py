from django.urls import path
from . import views
from .api import StudentList, CoachList, TeamList, TeamDetail

app_name = 'coaching_app'

urlpatterns = [
    path('', views.index, name='index'),
    
    # #students path
    # path('students/', views.student_list, name='student_list'),
    # path('students/<int:pk>', views.student_detail, name='student_detail'),

    # #coaches path
    # path('coaches/', views.coach_list, name='coach_list'),

    # teams path
    path('team/<int:pk>', views.team_view, name='team_view'),
    path('team/create', views.team_create, name='team_create'),
    path('team/<int:pk>/insert', views.team_insert, name='team_insert'),
    path('team/<int:pk>/kick', views.team_kick, name='team_kick'),
    path('team/<int:pk>/settings', views.team_settings, name='team_settings'),
    path('team/<int:pk>/settings/update', views.team_update, name='team_update'),
    path('team/<int:pk>/settings/delete', views.team_delete, name='team_delete'),
    # path('team/<int:pk>/insert_coach', views.team_insert_coach, name='team_insert_coach'),

    #api
    path('api/v1/students', StudentList.as_view()),
    path('api/v1/students/<int:pk>', StudentList.as_view()),

    path('api/v1/coaches', CoachList.as_view()),
    path('api/v1/coaches/<int:pk>', CoachList.as_view()),

    path('api/v1/teams', TeamList.as_view()),
    path('api/v1/teams/<int:pk>', TeamDetail.as_view()),
]
