import os
import shutil
from pathlib import Path
from django.db.models import Q
from django.db import connection
from django.core.management.base import BaseCommand
from Users.models import CustomUser


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        # Directories path
        ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
        MEDIA_FOLDER_PATH = os.path.join(ROOT_DIR, 'media')

        # Excluding other user if needed
        excluded_users_id = [str(CustomUser.objects.filter(is_superuser=True).first().id),]
        exclude_emails = input("Enter emails that need to be excluded (separate each email by ', '): ")
        splitted_exclude_emails = exclude_emails.split(',')

        for email in splitted_exclude_emails: # Getting id of excluded_users email
            user = CustomUser.objects.filter(email=email).first()

            if user:
                excluded_users_id.append(str(user.id))

        # Deleting all user except admin and users that are in "excluded_users_id"
        print("Deleting all users .....")
        users = CustomUser.objects.filter(Q(is_superuser=False) & ~Q(id__in=excluded_users_id))
        number_of_users_being_deleted = users.count()
        users.delete()

        for directory in os.listdir(MEDIA_FOLDER_PATH):
            if directory not in excluded_users_id:
                user_directory = os.path.join(MEDIA_FOLDER_PATH, directory)

                if os.path.isdir(user_directory):
                    shutil.rmtree(user_directory)

        with connection.cursor() as cursor:
            cursor.execute('VACUUM')

        print(f"\nSuccessfully removed {number_of_users_being_deleted} users :-)")

    def handle(self, *args, **options):
        self._create_tags()
