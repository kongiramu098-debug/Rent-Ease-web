from django.core.management.base import BaseCommand
from rentals.models import Shop, Product
class Command(BaseCommand):
    help = "Create sample rental shop and electronic products"
    def handle(self, *args, **kwargs):
        shop, _ = Shop.objects.get_or_create(name="TechRent Demo Store", defaults={"address":"Tirupati, Andhra Pradesh","city":"Tirupati"})
        samples = [
            ("Lenovo IdeaPad Laptop","Laptops","Lenovo","For study, coding and office work.",450,2000),
            ("Canon EOS Camera","Cameras","Canon","Digital camera for events and travel.",650,2500),
            ("Samsung Galaxy Smartphone","Smartphones","Samsung","Android smartphone for short-term use.",300,1000),
            ("Epson Projector","Projectors","Epson","Projector for presentations and events.",800,3000),
            ("Apple iPad Tablet","Tablets","Apple","Tablet for learning and media.",500,2000),
            ("JBL Bluetooth Speaker","Speakers","JBL","Portable speaker for small events.",150,500),
        ]
        for name,cat,brand,desc,price,deposit in samples:
            Product.objects.get_or_create(shop=shop,name=name,defaults={"category":cat,"brand":brand,"description":desc,"daily_price":price,"security_deposit":deposit,"quantity":2})
        self.stdout.write(self.style.SUCCESS("Demo shop and products are ready."))
