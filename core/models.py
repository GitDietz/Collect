from django.db import models


## Model Managers ## #
class CollectionTypeManager(models.Manager):
    def all(self):
        qs = super(CollectionTypeManager, self).all()
        return qs

    def active(self, group_id):
        qs = super(CollectionTypeManager, self).filter(active=True).filter(in_group=group_id)
        return qs


class CountryManager(models.Manager):
    def all(self):
        qs = super(CountryManager, self).all()
        return qs


# ## Models ## #
class CollectionType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    objects = CollectionTypeManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    currency = models.CharField(max_length=100, unique=False, blank=False, null=False)
    currency_code = models.CharField(max_length=4, blank=False, null=False)
    objects = CountryManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()
