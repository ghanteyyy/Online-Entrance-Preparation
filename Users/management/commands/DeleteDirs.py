import os
import shutil
from django.core.management.base import BaseCommand
from Users.models import *
from core.settings import BASE_DIR


class DeleteDirs:
    def Action(self):
        media_dir = str(BASE_DIR / 'media')

        dirs_in_media_dir = set(os.listdir(media_dir))
        dirs_in_db = set([str(user.id) for user in CustomUser.objects.all()])

        not_in_db = dirs_in_media_dir - dirs_in_db

        for _dir in not_in_db:
            to_delete = os.path.join(media_dir, _dir)

            if os.path.isdir(to_delete):
                shutil.rmtree(to_delete)
                print('Deleted dir: ', _dir)


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_tags(self):
        DeleteDirs().Action()

    def handle(self, *args, **options):
        self._create_tags()
