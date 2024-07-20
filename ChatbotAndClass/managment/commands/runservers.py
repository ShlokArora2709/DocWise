from django.core.management.base import BaseCommand
from django.core.management import call_command
import multiprocessing

def run_django():
    call_command('runserver', '127.0.0.1:8000')

def run_daphne():
    from daphne.cli import CommandLineInterface
    CommandLineInterface.entrypoint(argv=["daphne", "-u", "unix:/tmp/daphne.sock", "myproject.asgi:application"])

class Command(BaseCommand):
    help = 'Runs Django and Daphne servers simultaneously'

    def handle(self, *args, **kwargs):
        p1 = multiprocessing.Process(target=run_django)
        p2 = multiprocessing.Process(target=run_daphne)

        p1.start()
        p2.start()

        p1.join()
        p2.join()
