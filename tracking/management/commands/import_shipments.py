# tracking/management/commands/import_shipments.py
import csv
from django.core.management.base import BaseCommand
from tracking.models import Shipment, Article


class Command(BaseCommand):
    help = 'Import shipment data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        self.import_shipments(csv_file_path)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def import_shipments(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if Shipment.objects.filter(tracking_number=row['tracking_number']).exists():
                    shipment = Shipment.objects.get(tracking_number=row['tracking_number'])
                else:
                    shipment = Shipment.objects.create(
                        tracking_number=row['tracking_number'],
                        carrier=row['carrier'],
                        sender_address=row['sender_address'],
                        receiver_address=row['receiver_address'],
                        status=row['status'],
                    )
                Article.objects.create(
                    shipment=shipment,
                    name=row['article_name'],
                    quantity=row['article_quantity'],
                    price=row['article_price'],
                    SKU=row['SKU'],
                )
