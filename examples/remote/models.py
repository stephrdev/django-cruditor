import requests


BASE_TAG = {'id': 0, 'name': 'cruditor'}


class Pet:

    def __init__(self, pet):
        self.data = {
            'id': pet['id'],
            'name': pet['name'],
            'photo_url': pet['photoUrls'][0]
        }

    def __str__(self):
        return self.name

    @property
    def pk(self):
        return self.data['id']

    @property
    def name(self):
        return self.data['name']

    def for_form(self):
        return {
            'name': self.data['name'],
            'photo_url': self.data['photo_url']
        }

    def update(self, form):
        self.data = Pet(requests.put('http://petstore.swagger.io/v2/pet', json={
            'id': self.data['id'],
            'name': form['name'],
            'photoUrls': [form['photo_url']],
            'tags': [BASE_TAG],
            'status': 'available'
        }).json()).data

    def delete(self):
        requests.delete(
            'http://petstore.swagger.io/v2/pet/{}'.format(self.data['id']))

    @classmethod
    def get_list(cls):
        all_pets = requests.get(
            'http://petstore.swagger.io/v2/pet/findByStatus',
            {'status': 'available'}
        ).json()

        for pet in all_pets:
            # Filter pets with tag cruditor
            tags = pet.get('tags', [])
            if not tags or tags[0] != BASE_TAG:
                continue

            yield Pet(pet)

    @classmethod
    def get(cls, pk):
        return Pet(requests.get(
            'http://petstore.swagger.io/v2/pet/{}'.format(pk)).json())

    @classmethod
    def create(cls, form):
        return Pet(requests.post('http://petstore.swagger.io/v2/pet', json={
            'name': form['name'],
            'photoUrls': [form['photo_url']],
            'tags': [BASE_TAG],
            'status': 'available'
        }).json())
