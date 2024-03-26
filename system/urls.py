from django.urls import path

from .views import (ProfileUpdateView, ProfileDetailView, ProfileListView,
                    UserRegisterView, UserLoginView, UserLogoutView, UserPasswordChangeView,
                    UserForgotPasswordView, UserPasswordResetConfirmView,
                    EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView,
                    FeedbackCreateView, )

app_name = 'system'

urlpatterns = [

    path('user/list/', ProfileListView.as_view(), name='profile_list'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('user/<str:slug>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),

    path('login/', UserLoginView.as_view(redirect_authenticated_user=True, ), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),  # смена пароля если авторизован
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),  # сброс пароля
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # забыл пароль, если не авторизован

    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),

]
