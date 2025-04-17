from django.db import models

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    installed = models.BooleanField(default=False)
    version = models.CharField(max_length=10, default="1.0")
    installation_status = models.CharField(max_length=50, default="Not Installed")
    install_query = models.TextField(null=True, blank=True)
    delete_query = models.TextField(null=True, blank=True)

    def install(self):
        self.installed = True
        self.installation_status = "Installed"
        self.save()

    def uninstall(self):
        self.installed = False
        self.installation_status = "Not Installed"
        self.save()

    def upgrade(self, new_version):
        self.version = new_version
        self.installation_status = "Upgraded"
        self.save()

    def __str__(self):
        return f"{self.name} (v{self.version})"

