from django.db import models


class Shipment(models.Model):
    tracking_number = models.CharField(max_length=50, unique=True)
    carrier = models.CharField(max_length=50)
    sender_address = models.TextField()
    receiver_address = models.TextField()
    status = models.CharField(max_length=50)

    def get_articles(self):
        return Article.objects.filter(shipment=self)

    def get_destination_city(self):
        if len(self.receiver_address.split(',')) > 1:
            # if address is normal string
            destination = self.receiver_address.split(',')[1].split(' ')[2]
        else:
            # if address is zip code
            destination = self.receiver_address
        return destination

    def __str__(self):
        return self.tracking_number


class Article(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='articles')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    SKU = models.CharField(max_length=50)


