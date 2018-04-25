from django.db import models


class Person(models.Model):
    COUNTRIES = ('Germany', 'France', 'Italy')

    first_name = models.CharField('First name', max_length=64)
    last_name = models.CharField('Last name', max_length=64, blank=True)

    country = models.CharField(
        'Country', max_length=32, choices=zip(COUNTRIES, COUNTRIES))

    birthdate = models.DateField('Birthdate', blank=True, null=True)
    reminder = models.DateTimeField('Next reminder')
    approved = models.BooleanField('Is approved')
    stars = models.IntegerField('Stars', choices=zip(range(1, 6), range(1, 6)))

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self):
        if self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.first_name


class RelatedPerson(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    first_name = models.CharField('First name', max_length=64)
    last_name = models.CharField('Last name', max_length=64, blank=True)

    is_child = models.BooleanField('Is child')

    class Meta:
        verbose_name = 'Related person'
        verbose_name_plural = 'Related persons'

    def __str__(self):
        return '{} ({})'.format(self.first_name, self.person)
