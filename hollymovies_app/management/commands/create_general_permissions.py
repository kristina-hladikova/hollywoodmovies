from django.core.management import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from hollymovies_app.general_permissions import GENERAL_PERMISSIONS

class Command(BaseCommand):
    help = "Create general permissions for our hollymovies app"

    def handle(self, *args, **kwargs):
        content_type, _ = ContentType.objects.get_or_create(app_label='general_permission', model='GeneralPermission')
        for name, codename in GENERAL_PERMISSIONS.items():
            _, created = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=content_type
            )
            if created:
                print(f'Permission created {name}')
        print('\n')
        print('All permissions created')
