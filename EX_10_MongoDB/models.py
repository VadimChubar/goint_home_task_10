from mongoengine import Document, StringField, connect

connect(db='mongo_my_phonebook', host='mongodb://localhost:27017')


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    phone = StringField(max_length=20)
    email = StringField(max_length=50)
    comment = StringField(max_length=100)

