from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver

from ascii.textmode.models import ArtFile, ArtFileTag


@receiver(m2m_changed, sender=ArtFile.tags.through)
def update_artfiletag_count_on_change(sender, instance, action, pk_set, reverse, **kwargs):
    if reverse:
        raise NotImplementedError

    match action:
        case "pre_add":
            for tag in ArtFileTag.objects.filter(pk__in=pk_set):
                tag.artfile_count += 1
                tag.save(update_fields=["artfile_count"])
        case "pre_remove":
            for tag in ArtFileTag.objects.filter(pk__in=pk_set):
                tag.artfile_count -= 1
                tag.save(update_fields=["artfile_count"])
        case "pre_clear":
            for tag in instance.tags.all():
                tag.artfile_count -= 1
                tag.save(update_fields=["artfile_count"])


@receiver(pre_delete, sender=ArtFile)
def update_artfiletag_count_on_delete(sender, instance, **kwargs):
    for tag in instance.tags.all():
        tag.artfile_count -= 1
        tag.save(update_fields=["artfile_count"])
