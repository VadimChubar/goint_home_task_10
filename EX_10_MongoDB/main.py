from models import Contact
import argparse

parser = argparse.ArgumentParser(description='Phone Book')
parser.add_argument("--action", "-a", help="Command: create, remove, find, find_all")

parser.add_argument("--fullname")
parser.add_argument("--phone")
parser.add_argument("--email")
parser.add_argument("--comment")

args = vars(parser.parse_args())

action = args.get("action")
fullname = args.get("fullname")
phone = args.get("phone")
email = args.get("email")
comment = args.get("comment")


def main():

    match action:

        case "create":
            Contact(fullname=fullname, phone=phone, email=email, comment=comment).save()
            print(f"Contact created {fullname}")

        case "remove":
            f = fullname
            con_ = Contact.objects(fullname=fullname)
            con_.delete()
            print(f"Contact {f} deleted")

        case "find":
            con_ = Contact.objects(fullname=fullname)
            for i_ in con_:
                print(i_.to_mongo().to_dict())

        case "find_all":
            con_ = Contact.objects()
            for i_ in con_:
                print(i_.to_mongo().to_dict())

        case _:
            print("Unknown command!")


if __name__ == '__main__':
    main()
