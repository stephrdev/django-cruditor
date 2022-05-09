import factory
from django.utils import timezone
from factory import fuzzy

from examples.store.models import Person, RelatedPerson


class PersonFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    country = fuzzy.FuzzyChoice(Person.COUNTRIES)
    reminder = fuzzy.FuzzyDateTime(timezone.now())
    approved = fuzzy.FuzzyChoice((True, False))
    stars = fuzzy.FuzzyInteger(1, 6)

    class Meta:
        model = Person


class RelatedPersonFactory(factory.django.DjangoModelFactory):
    person = factory.SubFactory(PersonFactory)
    first_name = factory.Faker('name')
    is_child = fuzzy.FuzzyChoice((True, False))

    class Meta:
        model = RelatedPerson
