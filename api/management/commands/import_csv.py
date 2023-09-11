import csv
from django.core.management.base import BaseCommand, CommandError
from api.models import Store


class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        with open(csv_file) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                date, scrip, openingPrice, highPrice, lowPrice, closingPrice, volume = row
                Store.objects.create(
                    date=date,
                    scrip=scrip,
                    openingPrice=openingPrice,
                    highPrice=highPrice,
                    lowPrice=lowPrice,
                    closingPrice=closingPrice,
                    volume=volume,
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
