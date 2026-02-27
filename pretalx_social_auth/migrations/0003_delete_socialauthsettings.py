from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pretalx_social_auth", "0002_partial_association_code_nonce_usersocialauth"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SocialAuthSettings",
        ),
    ]
