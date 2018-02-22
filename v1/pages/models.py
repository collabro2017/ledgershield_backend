from django.db import models
from django.utils.text import slugify

from v1.general.models import TimedModel

class Page(TimedModel):

    name = models.CharField(db_index=True, unique=True, max_length=50)
    slug = models.SlugField(db_index=True, unique=True)
    content = models.TextField()

    class Meta:
        app_label = 'pages'



    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Page, self).save(*args, **kwargs)
