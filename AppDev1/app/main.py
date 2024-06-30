"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as mobile number, name, gender, date of birth, and company.

"""

from constants import *
from utilis.utility import *
from app.email.email_constants import *


def create_user(name, role=None):
    """
    These function is used to create user for Authentication and Authorisation
    :param name: str    :param role: str
    :return: bool
    """
    try:
        if not authenticate_user(name):
            log.warning(f"UnAuthorised user {name} trying to access the application")
            raise Exception(f"UnAuthorised user {name} trying to access the application")

        # Authorisation
        if name in ADMINS:
            log.info(f"User {name} admin authorization is successfull")
            print(f"Enter role normal user or admin user ?:")
            role = input(f"Options are normal, admin:")

            if role == 'normal':
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.info(f'Admin {name} has created the normal user')
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)

            elif role == 'admin':
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.info(f"Admin {name} has created the admin user")
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)
            else:
                raise ValueError(f"Incorrect role choosen - available options are normal and admin only")

        else:
            log.error(f"User={name} does not have create user profile permission")
            raise PermissionError(f"User {name} does not have create user profile permission")
    except ValueError as err:
        print(err)

    except PermissionError as err:
        print(err)

    except Exception as err:
        print(err)


def update_record(DATA):
    """
    This function update full records in DATA
    :param DATA: dict    :return DATA: dict
    """
    try:
        for item in range(len(DATA["records"])):
            log.info(f'{DATA["records"][item]["name"]}--> update_record function has started...')
            current_record = DATA["records"][item]

            log.info(f'"message:-Modifying {item + 1} record"')
            print(f'Updating {item + 1} record:-')
            Username = input(f"Enter the username for {item + 1} record :- ")
            Name = input(f"Enter name for {item + 1} record:- ")
            Gender = input(f'Enter the gender for {item + 1} record:-')
            Dept = input(f'Enter your Depeartment fro {item + 1} record:-')

            log.info(f'"message:- Previous record of {item + 1} is :-" {DATA["records"][item]}')

            if is_valid_name(Name):
                if is_valid_gender(Gender, Name):
                    current_record["username"] = Username
                    current_record["name"] = Name
                    ALL_USERS.append(Name)
                    current_record["gender"] = Gender
                    current_record["dept"] = Dept
                    log.info(f'"message:-" "Modified {item + 1} record is ":-{DATA["records"][item]}')
                    log.info(f'updated record is = {DATA}')
    except ValueError as err:
        print(err)

    except Exception as err:
        print(err)
    log.info(f'update_record function has ended...')
    return DATA


def update_user_record(DATA, name):
    try:
        log.info(f"update_user_record function has started....")
        for item in range(len(DATA["records"])):
            if name == DATA["records"][item]["name"]:
                log.info(f'user={name} data is in records')
                print(f'{name} has updating his record')

                current_record = DATA["records"][item]
                Username = input(f"Enter the username for {item + 1} record :- ")
                Name = input(f"Enter name for {item + 1} record:- ")
                Gender = input(f'Enter the gender for {item + 1} record:-')
                Dept = input(f'Enter your Department for {item + 1} record:-')

                log.info(f'Before updating the record = {DATA}')
                if is_valid_name(Name):
                    if is_valid_gender(Gender, Name):
                        current_record["username"] = Username
                        current_record["name"] = Name
                        current_record["gender"] = Gender
                        current_record["dept"] = Dept
                        log.info(f'After user updated his record = {DATA}')
                        print(f'Updated user={name} record = {DATA["records"][item]}')
    except ValueError as err:
        print(err)

    except Exception as err:
        print(err)
    log.info(f'update_user_record function has ended...')
    return DATA


def partial_update_record(DATA):
    """
    This function is used for partial update of records in DATA
    :param DATA: dict    :return DATA:  dict
    """
    try:
        for item in range(len(DATA["records"])):
            log.info(f'{DATA["records"][item]["name"]} --> partial_update_record function has started...')
            log.info(f'"message:-" "Partial Modifying {item + 1} record"')
            print(f'Partially updating {item + 1} record:-')

            Name = input(f"Enter name for {item + 1} record:- ")
            if is_valid_name(Name):
                DATA["records"][item]["name"] = Name

            log.info(f'"message:-" "Partial Modified {item + 1} record is ":-{DATA["records"][item]}')
    except Exception as err:
        print(err)
    log.info(f"Saved Record={DATA}")
    log.info("partial_update_record function has ended...")
    return f"partially updated saved record are={DATA}"


def delete_record(DATA):
    """
    This function will delete the record in DATA
    :param DATA: dict    :return DATA:  dict
    """
    log.info(f'delete_record function has started...')
    try:
        Name = input("Enter the name of user:- ")
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    del DATA["records"][item]
                    log.info(f'Deleted the {Name} record...')
                    print(f"Deleted the {Name} record...")
                    break
        else:
            raise Exception(f'user {Name} is not there...')

    except Exception as err:
        print(err)
    log.info(f'delete_record function has ended....')


def read_records():
    print(f'Saved Record = {DATA}')
    log.info(f'Saved Record = {DATA}')


name = input("Enter the name of user :-")
log.info(f"Entered name of user is = {name}")
if name in ADMINS:
    log.info(f"User={name} is an admin, having Admin properties")
    print(f"User={name} is an admin, having Admin properties")
elif name in USERS:
    print(f"User={name} is a user, having User properties. You only have access to read records in DATA")
    log.info(f"User={name} is a user, having User properties")
else:
    log.warning(f"Unauthorized User={name}, trying to access the application...")
    send_email([members for members in receivers], UNAUTHENTICATED_MESSAGE)
    print("Email is sent to respective team members")
    print(f"Unauthorized User={name}, trying to access the application...")
    exit()

while True:
    if name in ADMINS:
        options = int(input(
            f"Which Operation you need to perform \n1)Create User \n2)Update Record \n3)Partially Update Record \n4)Delete Record \n5)Read Records \n6)Exit \n Choose from above option:- "))
        if options == 1:
            log.info(f'Entered Option=1 "Create User"')
            create_user(name)
            send_email([members for members in receivers], CREATE_USER)
        elif options == 2:
            log.info(f'Entered Option=2 "Update Record"')
            print(update_record(DATA))
            send_email([members for members in receivers], UPDATE_MESSAGE)
        elif options == 3:
            log.info(f'Entered Option=3 "Partially update record"')
            print(partial_update_record(DATA))
            send_email([members for members in receivers], PARTIAL_UPDATE)
        elif options == 4:
            log.info(f'Entered Option=4 "delete record"')
            print(delete_record(DATA))
            send_email([members for members in receivers], DELETE_MESSAGE)
        elif options == 5:
            log.info(f'Entered Option=5 "Read Record"')
            print(read_records())
            send_email([members for members in receivers], GET_ALL_MESSAGE)
        elif options == 6:
            log.info(f'Entered Option=6 "Exit"')
            exit()
        else:
            log.info(f'Entered wrong Option={options}')
            print(f"Choosed wrong option ={options}")
            options = int(input(
                 f"Which Operation you need to perform \n1)Create User \n2)Update Record \n3)Partially Update Record \n4)Delete Record \n5)Read Records \n6)Exit \n Choose from above option:- "))

    elif name in USERS:
        options = int(input(
            f'Which operation need to perform \n1)Create User \n2)Update your record \n3)Read Record \n4)Exit \n Choose from above options :- '))
        if options == 1:
            log.info(f'Entered Option=1 "Create User"')
            create_user(name)
        elif options == 2:
            log.info(f'Entered Option=2 "Update your record"')
            send_email([members for members in receivers], UPDATE_USER_RECORD)
            update_user_record(DATA,name)
        elif options == 3:
            log.info(f'Entered Option=3 "Read record"')
            read_records()
            send_email([members for members in receivers],GET_ALL_MESSAGE)
        elif options == 4:
            log.info(f'Entered Option=4 "Exit"')
            break
        else:
            log.info(f'Entered wrong option={options}')
            print(f'Choosed wrong option ={options}')
            options = int(input(
                f'Which operation need to perform \n1)Create User \n2)Update your record \n3)Read Record \n4)Exit \n Choose from above options :- '))
    else:
        break
