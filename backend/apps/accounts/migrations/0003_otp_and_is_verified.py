from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def copy_verified_flags(apps, schema_editor):
    UserProfile = apps.get_model('accounts', 'UserProfile')
    UserProfile.objects.filter(email_verified=True).update(is_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_email_verify_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(default=False, verbose_name='Verified'),
        ),
        migrations.RunPython(copy_verified_flags, migrations.RunPython.noop),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('is_used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='otps',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'OTP',
                'verbose_name_plural': 'OTPs',
                'db_table': 'OTPs',
                'ordering': ['-created_at'],
            },
        ),
    ]
