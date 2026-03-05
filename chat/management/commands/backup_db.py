import os
import shutil
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Efectúa una copia de seguridad (Backup regular) de la base de datos local SQLite.'

    def handle(self, *args, **kwargs):
        db_path = settings.DATABASES['default']['NAME']
        
        # Make a backup folder if doesn't exist
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f'db_backup_{timestamp}.sqlite3')
        
        try:
            shutil.copy2(db_path, backup_file)
            self.stdout.write(self.style.SUCCESS(f'Backup exitoso: {backup_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error realizando backup: {e}'))
