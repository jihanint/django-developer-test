from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.utils import OperationalError, ProgrammingError

class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name

def create_roles():
    try:
        if not ContentType.objects.filter(model="product").exists():
            return  

        content_type = ContentType.objects.get_for_model(Product)

        manager_group, _ = Group.objects.get_or_create(name="Manager")
        user_group, _ = Group.objects.get_or_create(name="User")
        public_group, _ = Group.objects.get_or_create(name="Public")

        # Assign permissions only if they are missing
        all_permissions = Permission.objects.filter(content_type=content_type)
        manager_group.permissions.add(*all_permissions)

        user_permissions = all_permissions.exclude(codename__startswith="delete_")
        user_group.permissions.add(*user_permissions)

        public_permissions = all_permissions.filter(codename__startswith="view_")
        public_group.permissions.add(*public_permissions)

    except (OperationalError, ProgrammingError):
        print("Skipping role creation because the database is not ready.")
