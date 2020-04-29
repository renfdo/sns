from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import os, time, datetime
from api.views import exec_flow


class Command(BaseCommand):
    help = 'Run and debug flow process'

    def handle(self, *args, **options):
        dt = "2019-10-10"
        exec_flow(dt)

        