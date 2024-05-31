import os
import datetime
import uuid

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.dispatch import receiver

from .utils import make_thumbnail, attach_xmp


class LicenceType(models.Model):
    name = models.CharField(max_length=255)
    html = models.CharField(max_length=2000)
    xmp_file = models.FileField(default='', upload_to='licences/')

    def __str__(self):
        return self.name


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
    return f"images/thumbnail/{instance.group.id}/{uuid.uuid4()}{os.path.splitext(filename)[1]}"


class Image(models.Model):
    group = models.ForeignKey(ImageGroup, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='', blank=True)
    description = models.CharField(max_length=255, default='', blank=True)
    image_original = models.ImageField(default='', upload_to=original_directory_path)
    image_thumbnail = models.ImageField(default='', upload_to=thumbnail_directory_path, blank=True)
    publication_date = models.DateTimeField("date published", default=timezone.datetime(1990, 1, 1))
    licence = models.ForeignKey(LicenceType, on_delete=models.PROTECT)

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
        current_thumbnail_path = self.image_thumbnail.path
        expected_thumbnail_path = self.image_original.path.replace('/original/', '/thumbnail/')
        if current_thumbnail_path != expected_thumbnail_path:
            os.rename(current_thumbnail_path, expected_thumbnail_path)
            self.image_thumbnail.name = self.image_original.name.replace('/original/', '/thumbnail/')
            super().save(*args, update_fields=['image_thumbnail'], **kwargs)

        if len(self.licence.xmp_file.name) > 0:
            attach_xmp(self.image_original.path, self.licence.xmp_file.path)
            attach_xmp(expected_thumbnail_path, self.licence.xmp_file.path)


# https://stackoverflow.com/a/16041527
# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Image` object is deleted.
    """
    if instance.image_original and len(instance.image_original.name) > 0:
        if os.path.isfile(instance.image_original.path):
            os.remove(instance.image_original.path)

    if instance.image_thumbnail and len(instance.image_thumbnail.name) > 0:
        if os.path.isfile(instance.image_thumbnail.path):
            os.remove(instance.image_thumbnail.path)


@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Image` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        image_entry = Image.objects.get(pk=instance.pk)
    except Image.DoesNotExist:
        return False

    old_file = image_entry.image_original
    if len(old_file.name) > 0:
        new_file = instance.image_original
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    old_file = image_entry.image_thumbnail
    if len(old_file.name) > 0:
        new_file = instance.image_thumbnail
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
