from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.timezone import now as tz_now

UserModel = get_user_model()

PUBLISH_CHOICES = (
    ('draft', 'Draft'),
    ('publish', 'Publish'),
    ('private', 'Private'),
)


class Post(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE,
                               verbose_name='Post author', related_name='posts')
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    publish = models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
    publish_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return smart_text(self.title)


@receiver(pre_save, sender=Post)
def blog_post_pre_save_handler(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance:
        # Update the slug field only when title is available and slug field value is not set
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
        # Update the publish_date in-case the post is changed to publish
        if instance.publish == 'publish':
            instance.publish_date = tz_now()
