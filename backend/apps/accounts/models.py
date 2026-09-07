from datetime import timedelta
from django.db import models
from django.conf import settings
from django.utils import timezone
import secrets


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    email_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField('Verified', default=False)
    email_verify_token = models.CharField(max_length=64, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username

    def mark_verified(self):
        self.is_verified = True
        self.email_verified = True
        self.email_verify_token = ''
        self.save(update_fields=['is_verified', 'email_verified', 'email_verify_token'])

    def issue_verify_token(self):
        self.email_verify_token = secrets.token_urlsafe(32)
        self.save(update_fields=['email_verify_token'])
        return self.email_verify_token


class OTP(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='otps',
    )
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'OTPs'
        ordering = ['-created_at']
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return f'{self.user_id} · {self.code}'

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @classmethod
    def issue_for(cls, user):
        minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        return cls.objects.create(
            user=user,
            code=f'{secrets.randbelow(1_000_000):06d}',
            expires_at=timezone.now() + timedelta(minutes=minutes),
        )

    @classmethod
    def match_for_user(cls, user, code):
        cleaned = (code or '').strip()
        if len(cleaned) != 6 or not cleaned.isdigit():
            return None
        otp = (
            cls.objects.filter(user=user, is_used=False, code=cleaned)
            .order_by('-created_at')
            .first()
        )
        if otp is None or otp.is_expired:
            return None
        return otp
