import os
import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib import admin

from .utils import make_thumbnail
from mysite.settings import MEDIA_ROOT  # probably not the right way to do it


class ImageGroup(models.Model):
    name = models.CharField(max_length=255)
    publication_date = models.DateTimeField("date published")

    def __str__(self):
        return self.name

    @admin.display(
        boolean=False,
        ordering="publication_date",
        description="Elapsed days since published",
    )
    def days_since_published(self):
        now = timezone.now()
        return (now - self.publication_date).days


def original_directory_path(instance, filename):
    return f"images/original/{instance.group.id}/{uuid.uuid4()}{os.path.splitext(filename)[1]}"


def thumbnail_directory_path(instance, filename):
    print('thumbnail_directory_path')
    return f"images/thumbnail/{instance.group.id}/{uuid.uuid4()}{os.path.splitext(filename)[1]}"


class Image(models.Model):
    group = models.ForeignKey(ImageGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='', blank=True)
    description = models.CharField(max_length=255, default='', blank=True)
    image_original = models.ImageField(default='', upload_to=original_directory_path)
    image_thumbnail = models.ImageField(default='', upload_to=thumbnail_directory_path, blank=True)
    publication_date = models.DateTimeField("date published", default=timezone.datetime(1990, 1, 1))

    def __str__(self):
        return self.title

    @admin.display(
        boolean=True,
        ordering="publication_date",
        description="Elapsed days since published",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.publication_date <= now

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # probably not the right way to do it
        if self.image_thumbnail.name == '':
            # create thumbnail and save it with auto-naming
            self.image_thumbnail = make_thumbnail(self.image_original)
            super().save(*args, update_fields=['image_thumbnail'], **kwargs)

        # edit thumbnail naming and rename file
        os.rename(os.path.join(MEDIA_ROOT, self.image_thumbnail.name),
                  os.path.join(MEDIA_ROOT, self.image_original.name).replace('/original/', '/thumbnail/'))
        self.image_thumbnail.name = self.image_original.name.replace('/original/', '/thumbnail/')
        super().save(*args, update_fields=['image_thumbnail'], **kwargs)
