import argparse
from functools import wraps

from bson import ObjectId
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client.mynotesdb

parser = argparse.ArgumentParser(description='My Phone Book')
parser.add_argument('--action', help='Command: create, update, find, remove')
parser.add_argument('--id')
parser.add_argument('--fullname')
parser.add_argument('--phone')
parser.add_argument('--email')
parser.add_argument('--note', nargs='+')

arguments = parser.parse_args()
my_arg = vars(arguments)

action = my_arg.get('action')
fullname = my_arg.get('fullname')
phone = my_arg.get('phone')
email = my_arg.get('email')
_id = my_arg.get('id')
note = my_arg.get('note')


class ExceptValidation(Exception):
    pass


def validate(func):
    @wraps(func)
    def wrapper(*args):
        for el in args:
            if el is None:
                raise ExceptValidation(f"Error input {func.__name__}{args}")
        result = func(*args)
        return result
    return wrapper


def find_by_id(_id):
    result = db.cats.find_one({"_id": ObjectId(_id)})
    return result


def find():
    return db.cats.find()


@validate
def create(fullname, phone, email, note):
    result_one = db.cats.insert_one(
        {
            "fullname": fullname,
            "phone": phone,
            "email": email,
            "note": note,
        }
    )
    return find_by_id(result_one.inserted_id)


@validate
def update(_id, fullname, phone, email, note):
    db.cats.update_one({"_id": ObjectId(_id)}, {"$set": {
            "fullname": fullname,
            "phone": phone,
            "email": email,
            "note": note,
        }})
    return find_by_id(_id)


@validate
def remove(_id):
    db.cats.delete_one({"_id": ObjectId(_id)})
    return find_by_id(_id)


def main():
    try:
        match action:
            case 'create':
                r = create(fullname, phone, email, note)
                print(r)
            case 'find':
                r = find()
                [print(el) for el in r]
            case 'update':
                r = update(_id, fullname, phone, email, note)
                print(r)
            case 'remove':
                r = remove(_id)
                print(r)
            case _:
                print("Unknowns command")

    except ExceptValidation as err:
        print(err)


if __name__ == '__main__':
    main()