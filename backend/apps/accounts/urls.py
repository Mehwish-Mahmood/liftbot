from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', views.EmailLogoutView.as_view(), name='logout'),
    path('verify-email/', views.VerifyOtpView.as_view(), name='verify_otp'),
    path('verify-email/send/', views.SendOtpView.as_view(), name='send_otp'),
    path('verify-email/resend/', views.ResendVerificationView.as_view(), name='resend_verification'),
    path('verify-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('password-reset/', views.LiftbotPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.LiftbotPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.LiftbotPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.LiftbotPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
