from django.db import models
from django.utils.text import slugify

class Site(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug= models.SlugField(unique=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Link(models.Model):
    class Vendor(models.TextChoices):
        CERAGON = "CERAGON", "Ceragon"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DOWN = "DOWN", "Down"
        PLANNED = "PLANNED", "Planned"
        
    site_a = models.ForeignKey(Site, related_name="links_a", on_delete=models.PROTECT)
    site_b = models.ForeignKey(Site, related_name="links_b", on_delete=models.PROTECT)
    frequency_ghz = models.DecimalField(max_digits=5, decimal_places=2)
    capacity_mbps = models.PositiveIntegerField()
    vendor = models.CharField(max_length=20, choices=Vendor.choices, default=Vendor.CERAGON)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(site_a=models.F("site_b")), name="link_not_loop")
        ]
        indexes = [
            models.Index(fields=["vendor"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self): 
        return f"{self.site_a} ↔ {self.site_b}"

# Create your models here.
