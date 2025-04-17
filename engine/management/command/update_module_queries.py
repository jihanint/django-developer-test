from django.core.management.base import BaseCommand
from engine.models import Module

class Command(BaseCommand):
    help = 'Update install_query and delete_query for product_module'

    def handle(self, *args, **kwargs):
        install_query = '''
            CREATE TABLE IF NOT EXISTS "product_module_product" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "name" varchar(255) NOT NULL,
                "barcode" varchar(50) NOT NULL UNIQUE,
                "price" decimal NOT NULL,
                "stock" integer unsigned NOT NULL CHECK ("stock" >= 0)
            )
        '''
        delete_query = 'DROP TABLE IF EXISTS "product_module_product"'

        try:
            module = Module.objects.get(id=1)
            module.install_query = install_query
            module.delete_query = delete_query
            module.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated product_module queries'))
        except Module.DoesNotExist:
            self.stdout.write(self.style.ERROR('Module product_module does not exist'))