import logging

from apps.common.management.commands.data_script import CreateData
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def init():
    CreateData()


class Command(BaseCommand):
    help = "Populate the database with fake data"

    def handle(self, *args, **kwargs):
        try:
            self.stdout.write("Creating initial data...")
            init()
            self.stdout.write(
                self.style.SUCCESS("✅ Initial data created successfully")
            )
        except Exception as e:
            logger.exception("Failed to create initial data")
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to create initial data: {str(e)}")
            )
            raise
