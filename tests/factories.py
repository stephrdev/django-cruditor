import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda i: 'user{0}'.format(i))
    email = factory.LazyAttribute(lambda o: '{0}@none.none'.format(o.username))
    first_name = factory.Sequence(lambda i: 'First {0}'.format(i))
    last_name = factory.Sequence(lambda i: 'Last {0}'.format(i))

    class Meta:
        model = User
