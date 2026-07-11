from django.core.management.base import BaseCommand
from core.models import Category, Product


class Command(BaseCommand):
    help = 'Fill the database with sample categories and products'

    def handle(self, *args, **options):
        categories_data = {
            'Футболки': ['S', 'M', 'L', 'XL'],
            'Худи': ['S', 'M', 'L', 'XL'],
            'Джинсы': ['28', '30', '32', '34'],
            'Кроссовки': ['40', '41', '42', '43'],
        }

        products_data = [
            ('Футболки', 'Базовая белая футболка', 5000),
            ('Футболки', 'Футболка Oversize чёрная', 6500),
            ('Футболки', 'Футболка с принтом', 7000),
            ('Худи', 'Худи серый меланж', 15000),
            ('Худи', 'Худи чёрный oversize', 17000),
            ('Джинсы', 'Джинсы прямого кроя', 18000),
            ('Джинсы', 'Джинсы skinny синие', 16000),
            ('Кроссовки', 'Кроссовки белые классика', 25000),
            ('Кроссовки', 'Кроссовки чёрные спорт', 22000),
        ]

        for name, sizes in categories_data.items():
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'slug': name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f'Created category: {name}')

        for category_name, product_name, price in products_data:
            category = Category.objects.get(name=category_name)
            sizes = categories_data[category_name]
            for size in sizes:
                product, created = Product.objects.get_or_create(
                    name=f'{product_name} ({size})',
                    defaults={
                        'category': category,
                        'description': f'{product_name} — размер {size}',
                        'price': price,
                        'size': size,
                        'stock': 10,
                        'is_available': True,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))