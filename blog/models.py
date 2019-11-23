from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from PIL import Image
from io import BytesIO
import os

def validate_image(value):
    file = BytesIO(value.read())
    filesize = file.getbuffer().nbytes
    if filesize <= 150:
        raise ValidationError(_('Image size can\'t be zero.'))
    try:
        im = Image.open(file)
        if im.format not in ('BMP', 'PNG', 'JPEG'):
            raise ValidationError(_('Unsupported file extension.'))
        im.verify()
        im.close()
    except Exception as e:
        raise ValidationError(_("cannot identify image file"))


class Media(models.Model):
    class Meta:
        verbose_name = "Media for posts"
        verbose_name_plural = "Medias for posts"
    
    name = models.CharField(_("name"), max_length=80)
    pic = models.FileField(_("picture"), upload_to="posts_medias", validators=[validate_image])
    pic_alter = models.CharField(_("picture alternative"), max_length=75, null=True, blank=True, help_text="It's the alt attrbiute of the img (image).")


    def __str__(self) -> str:
        return self.name


@receiver(models.signals.post_delete, sender=Media)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.pic:
        if os.path.isfile(instance.pic.path):
            os.remove(instance.pic.path)


class Category(models.Model):
    class Meta:
        verbose_name = "Posts category"
        verbose_name_plural = "Posts Categories"
    name = models.CharField(_("name"), max_length=255)
    slug = models.SlugField(_("slug"),max_length=80, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    class Meta:
        get_latest_by = "id"
    title = models.CharField(_("title"), max_length=250)
    slug = models.SlugField(_("slug"), max_length=80, unique=True)
    body = models.TextField(_("body"))
    pic = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self) -> str:
        return self.title