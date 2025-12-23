from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),

    #activate url for user registation activation
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    #forgot password
    path('forgotPassword', views.forgotPassword, name='forgotPassword'),
    #reset password link validation
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    #reset password page
    path('resetPassword', views.resetPassword, name='resetPassword'),

    # my orders
    path('my_orders/', views.my_orders, name='my_orders'),

    #profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    #change password
    path('change_password/', views.change_password, name='change_password'),
    
    #order detail
    path('order_detail/<int:order_id>', views.order_detail, name='order_detail'),

]