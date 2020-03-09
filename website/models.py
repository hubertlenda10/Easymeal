from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Comment


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(null=True)
    image = models.ImageField(null=True, blank=True, upload_to='post_pics')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostComment(Comment):
    created_by = models.ForeignKey(User, related_name='post_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    date_created = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)
    url = models.URLField()
    image_url = models.URLField()

    class Meta:
        verbose_name = "News Item"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        super().save(**kwargs)
