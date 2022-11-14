import os
import argparse, sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_pdf.settings')
import django
from django.contrib.auth import authenticate

django.setup()
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType

from django_pdf.models import Report, UserData
from django_pdf.user_data import create_users_data, create_reports

GROUPS = {
    'ADMINS': {'name': 'ADMINS',
               'permissions': [{'code_name': 'view_report', 'model': Report},
                               {'code_name': 'create_report_pdf', 'model': Report},
                               {'code_name': 'create_user_data', 'model': UserData}]},
    'USERS': {'name': 'USERS', 'permissions': [{'code_name': 'view_report', 'model': Report}]}
}


def create_groups():
    for group_name in GROUPS.keys():
        group, created = Group.objects.get_or_create(name=GROUPS[group_name]['name'])
        # group.delete()
        if created:
            print(f'Creating group {group}.')
            for perm in GROUPS[group_name]['permissions']:
                ct = ContentType.objects.get_for_model(perm['model'])
                _permission = Permission.objects.get(codename=perm['code_name'], content_type=ct)
                group.permissions.add(_permission)
            group.save()
        print(f'Group {group} created.')


def create_user(username: str, email: str, password: str, group_name: str):
    user = User.objects.create_user(username=username, email=email, password=password)
    group = Group.objects.get_by_natural_key(group_name)
    user.groups.set([group])
    user.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("action")
    parser.add_argument("--username", help="username")
    parser.add_argument("--email", help="email")
    parser.add_argument("--password", help="password")
    parser.add_argument("--group", help="group")

    # Create user data
    parser.add_argument("--years", help="No of years to generate data for.")
    parser.add_argument("--no_of_users", help="No of users to generate data for.")
    parser.add_argument("--destination", help="Target dir to store generated data.")
    parser.add_argument("--categoriesfile", help="Source file to load categories.")

    args = parser.parse_args()
    # create_groups()

    if args.action == "createuser":
        if args.username:
            print(f'Create user {args.username}')
            create_user(username=args.username, email=args.email, password=args.password, group_name=args.group)
    if args.action == "createuserdata":
        years = int(args.years or "1")
        no_of_users = int(args.no_of_users or "1")
        create_users_data(no_of_users, args.destination, args.categoriesfile, years)

    if args.action == "createreports":
        create_reports(args.destination)
