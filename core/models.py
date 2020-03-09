from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Comment(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(null=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def approve(self):
        self.approved_comment = True
        self.save()

    def save(self, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        super().save(**kwargs)

    def __str__(self):
        return self.text
