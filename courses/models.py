from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    CATEGORIES = [
        ("basic", "Basic Maintenance"),
        ("advanced", "Advanced Repairs"),
        ("electric", "Electric Bikes"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # usado para URL amigável
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    level = models.CharField(max_length=20, choices=LEVELS)
    duration_hours = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
