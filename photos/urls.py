from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login/', views.loginpage, name='loginpage'),
    path('profile/', views.profile, name='profile'),
    path('save_profile/<int:pk>/', views.save_profile, name='save_profile'),
    path('create_userinfo/<int:pk>/', views.create_userinfo, name='create_userinfo'),
    path('staff-profile/', views.staff_profile, name='staff_profile'),
    path('logout/', views.logout_view, name='logout'),
    # path('signup/', views.signup, name='signup'),
    url(r'^password/$', views.change_password, name='change_password'),
    path('add_member/', views.add_member, name='add_member'),
    path('popup/', views.popup, name='popup'),
    path('img_download/<int:year>/<int:sem>/', views.img_download, name='img_download'),
    path('img_download_page/', views.img_download_page, name='img_download_page'),
    path('user_check/', views.user_check, name='user_check'),
    #path('mileage/', views.mileage, name='mileage'),
    path('no_student_id/<int:pk>/', views.no_student_id, name='no_student_id'),
    path('delete_userinfo/', views.delete_userinfo, name='delete_userinfo'),
    path('delete_userinfo_confirm/<int:year>/<int:sem>/<int:group_no>/', views.delete_userinfo_confirm, name='delete_userinfo_confirm'),
    # made by Group5 - Sumi(21700520@handong.edu) to add new feature 'register' (2021-06-03)
    path('register_form/', views.register_form, name='register_form')
]
  
    
    # 아래 두 라인 또한 urlpatterns 에 들어가야 하나, 다음과 같은 에러 발생하여 임의로 주석처리해둠 - 21500740@handong.edu
    #   File "/home/wooseokyourself/Histudy-issue4/photos/urls.py", line 25, in <module>
    #     path('group_match/', views.group_match, name='group_match'), 
    # AttributeError: module 'photos.views' has no attribute 'group_match'
    
    # made by Group5 - Sumi(21700520@handong.edu) to add new feature 'group_match' (2021-06-05)
    # path('group_match/', views.group_match, name='group_match'),
    # path('group_match_result/', views.group_match_result, name='group_match_result')
