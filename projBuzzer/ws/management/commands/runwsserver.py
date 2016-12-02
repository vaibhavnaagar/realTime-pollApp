from django.core.management.base import BaseCommand

from ws.server import run_server
from django.conf import settings

class Command(BaseCommand):
    help = "Runs websocket-based server."
    args = '[optional port number]'

    def add_arguments(self, parser):
        parser.add_argument('port', type=int, default=8080)

    def handle(self, *args, **options):
        port = options['port']
        run_server(settings.IP, port)
