from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Article


@receiver(post_save, sender=Article)
def create_article(sender, instance=None, created=False, **kwargs):
    if created:
        tags = instance.tags.all()
        for tag in tags:
            tag.article_count += 1
            tag.save(update_fields=['article_count'])


@receiver(post_delete, sender=Article)
def delete_article(sender, instance=None, **kwargs):
    tags = instance.tags.all()
    for tag in tags:
        tag.article_count -= 1
        tag.save(update_fields=['article_count'])
