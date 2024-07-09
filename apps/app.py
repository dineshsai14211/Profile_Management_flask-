"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as username,name, gender, date of birth, and company,dept.

"""
from log.logging_logic import *
from emails.email_operations import *
from utilis.utility import *
from constants import *


@authenticate
def create_user(name, role=None):
    """
    These function is used to create user for Authentication and Authorisation
    :param name: str    :param role: str
    :return: bool
    """
    log.info(f'create_user function has started...')
    try:
        # Authorisation
        if name in ADMINS:
            role = input(f"Options are normal, admin:")

            if role == 'normal':
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.info(f'Admin {name} has created the normal user')
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)
                    send_email([members for members in receivers],
                               RECORD_ADDED.format(name, user_info["name"], user_info))
                    print(f"New User={user_info["name"]} record added..")

            elif role == 'admin':
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.info(f"Admin {name} has created the admin user")
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)
                    send_email([members for members in receivers],
                               RECORD_ADDED.format(name, user_info["name"], user_info))
                    print(f"New User={user_info["name"]} record added..")

            else:
                raise ValueError(f"Incorrect role choosen - available options are normal and admin only")

        else:
            log.error(f"User={name} does not have create user profile permission")
            raise PermissionError(f"User {name} does not have create user profile permission")
    except ValueError as err:
        log.error(err)
        log.info(f'create_user function has ended...')

    except PermissionError as err:
        log.error(err)
        log.info(f'create_user function has ended...')

    except Exception as err:
        log.error(err)
        log.info(f'create_user function has ended...')


@authenticate
def update_record(name):
    """
    This function update full records in DATA
    :param name: str    :return DATA: dict
    """
    try:
        Name = input(f"Enter the name of user, to modify his record:-")
        log.info(f'Admin has entered name is {Name}')
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                log.info(f'update_record function has started...')
                current_record = DATA["records"][item]
                if Name == current_record["name"]:

                    log.info(f'"message:-Modifying User={Name} record"')
                    print(f'Updating User={Name}  record:-')
                    Username = input(f"Enter the username for User={Name}  record :- ")
                    Name = input(f"Enter name for User={Name}  record:- ")
                    Gender = input(f'Enter the gender for User={Name}  record:-')
                    Dept = input(f'Enter your Depeartment fro User={Name}  record:-')

                    log.info(f'"message:- Previous record of User={Name}  is :-" {DATA["records"][item]}')

                    if is_valid_name(Name):
                        if is_valid_gender(Gender, Name):
                            current_record["username"] = Username
                            current_record["name"] = Name
                            ALL_USERS.append(Name)
                            current_record["gender"] = Gender
                            current_record["dept"] = Dept
                            log.info(f'"message:-" "Modified User={Name}  record is ":-{DATA["records"][item]}')
                            send_email([members for members in receivers],
                                       UPDATE_MESSAGE.format(name, Name, DATA["records"][item]))
                            log.info(f'updated record is = {DATA}')
        else:
            log.error(f'Entered user={Name} has no records')
            print(f'Entered user={Name} has no records')

    except ValueError as err:
        log.error(err)
        log.info(f'update_record function has ended...')

    except Exception as err:
        log.info(f'update_record function has ended...')
        log.error(err)
    log.info(f'update_record function has ended...')
    return DATA


@authenticate
def update_user_record(name):
    try:
        log.info(f"update_user_record function has started....")
        for item in range(len(DATA["records"])):
            if name == DATA["records"][item]["name"]:
                log.info(f'user={name} data is in records')
                print(f'{name} has updating his record')

                current_record = DATA["records"][item]
                Username = input(f"Enter the username for {item + 1} record :- ")
                Gender = input(f'Enter the gender for {item + 1} record:-')
                Dept = input(f'Enter your Department for {item + 1} record:-')

                log.info(f'Before updating the record = {DATA}')

                if is_valid_gender(Gender, name):
                    current_record["username"] = Username
                    current_record["gender"] = Gender
                    current_record["dept"] = Dept
                    log.info(f'After user updated his record = {DATA}')
                    send_email([members for members in receivers],
                               UPDATE_USER_RECORD.format(name,DATA["records"][item]))
                    print(f'Updated user={name} record = {DATA["records"][item]}')
    except ValueError as err:
        log.error(err)
        log.info(f"update_user_record function has started....")

    except Exception as err:
        log.error(err)
        log.info(f"update_user_record function has started....")
    log.info(f'update_user_record function has ended...')
    return DATA


@authenticate
def partial_update_record(name):
    """
    This function is used for partial update of records in DATA
    :param name: dict    :return DATA:  dict
    """
    try:
        Name = input(f"Enter the name of user, to partially update his record = ")
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    log.info(f'For User={Name} --> partial_update_record function has started...')
                    log.info(f'"message:-" "Partial Modifying "{Name}" record"')
                    print(f'Partially updating "{Name}" record:-')

                    Name = input(f'Enter name for "{Name}" record:- ')
                    if is_valid_name(Name):
                        DATA["records"][item]["name"] = Name
                        ALL_USERS.append(Name)
                        send_email([members for members in receivers],
                                   PARTIAL_UPDATE.format(name, Name, DATA["records"][item]))
                        log.info(f'"message:-" "Partial Modified "{Name}" record is ":-{DATA["records"][item]}')

        else:
            log.error(f'Entered user={Name} has no records')
            print(f'Entered user={Name} has no records')

    except Exception as err:
        log.error(err)
        log.info("partial_update_record function has ended...")

    log.info(f"Saved Record={DATA}")
    log.info("partial_update_record function has ended...")
    return f"partially updated saved record are={DATA}"


@authenticate
def reset_password(name):
    """
    These function is used to reset the user password
    :param name: str
    """
    log.info(f'reset_password function has started...')
    try:
        Name = input(f'Enter the name of User,to reset his password = ')
        log.info(f'Admin enterd user name is "{Name}"')
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    Password = input(
                        "Enter the password that should contain one uppercase,lowercase,digit,special character = ")
                    log.info(f'Admin changed user={Name} password to "{Password}"')
                    if is_valid_password(Password):
                        log.info(
                            f'Before the reset password User={Name} password is "{DATA['records'][item]['password']}"')
                        DATA["records"][item]["password"] = Password
                        send_email([members for members in receivers],RESET_PASSWORD.format(name,Name))
                        log.info(
                            f'After the reset password User={Name} password is "{DATA['records'][item]['password']}"')
        else:
            print(f"User={Name} record is not there")
            log.warning(f"User={Name} record is not there")
    except Exception as err:
        log.error(err)
        log.info(f'reset_password function has ended...')
    log.info(f'reset_password function has ended...')


@authenticate
def user_info(name):
    """
    These function is about checking user detailed information.
    if user is admin,can see any user information
    if normal user,can see only his information
    :param name: str
    :return: dict
    """
    log.info(f'user_info function started...')
    try:
        if name in ADMINS:
            Name = input("Enter the name of user to see his details:- ")
            log.info(f'Admin={name} has entered "{Name}" to see his information')
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        print(f"User={Name} information :- {DATA["records"][item]}")
                        send_email([members for members in receivers],
                                   CHECK_USER_INFO.format(name,Name))
                        log.info(f"User={Name} information :- {DATA["records"][item]}")
            else:
                log.error(f"User={Name},is not in records")
                raise Exception(f"User={Name},is not in records")

        if name in USERS:
            log.info(f"User={name} having checking his information")
            for item in range(len(DATA["records"])):
                if name == DATA["records"][item]["name"]:
                    print(f"Your information :- {DATA["records"][item]}")
                    send_email([members for members in receivers],
                               CHECK_USER_INFO.format(name, Name))
                    log.info(f"Your information :- {DATA["records"][item]}")
    except Exception as err:
        log.error(err)
        log.info(f'user_info function ended...')
    log.info(f'user_info function ended...')


@authenticate
def delete_record(name):
    """
    This function will delete the record in DATA
    :param name: dict    :return DATA:  dict
    """
    log.info(f'delete_record function has started...')
    try:
        Name = input("Enter the name of user:- ")
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    del DATA["records"][item]
                    ALL_USERS.remove(Name)
                    send_email([members for members in receivers],
                               DELETE_MESSAGE.format(name,Name))
                    log.info(f'Deleted the {Name} record...')
                    print(f"Deleted the {Name} record...")
                    break
        else:
            raise Exception(f'user {Name} is not there...')

    except Exception as err:
        log.error(err)
        log.info(f'delete_record function has ended....')
    log.info(f'delete_record function has ended....')


@authenticate
def read_records(name):
    print(f'Saved Record = {DATA}')
    send_email([members for members in receivers], GET_ALL_MESSAGE.format(name))
    log.info(f'Saved Record = {DATA}')


def restart_program():
    name = input("Enter the name of user :-")
    log.info(f"Entered name of user is = {name}")
    if name in ADMINS:
        log.info(f"User={name} is an admin, having Admin properties")
        print(f"User={name} is an admin, having Admin properties")
    elif name in USERS:
        print(f"User={name} is a user, having User properties.")
        log.info(f"User={name} is a user, having User properties")
    else:
        log.warning(f"Unauthorized User={name}, trying to access the application...")
        send_email([members for members in receivers], UNAUTHENTICATED_MESSAGE.format(name))
        print(f"Email is sent to respective team members. \n Unauthorized User={name}, trying to access the application...")
        exit()

    while True:
        if name in ADMINS:
            options = int(input(ADMIN_CONSOLE))
            if options == 1:
                log.info(f'Entered Option=1 "Create User"')
                create_user(name)
            elif options == 2:
                log.info(f'Entered Option=2 "Update Record"')
                print(update_record(name))

            elif options == 3:
                log.info(f'Entered Option=3 "Partially update record"')
                print(partial_update_record(name))
            elif options == 4:
                log.info(f'Entered Option=4 "Check specify user info"')
                user_info(name)
            elif options == 5:
                log.info(f'Entered Option=5 "Delete Record"')
                delete_record(name)
            elif options == 6:
                log.info(f'Entered Option=6 "Reset User Password"')
                reset_password(name)
            elif options == 7:
                log.info(f'Entered Option=6 "Read Record"')
                read_records(name)
            elif options == 8:
                if restart(options):
                    restart_program()
                else:
                    exit()
            else:
                log.info(f'Entered wrong Option={options}')
                print(f"Choosed wrong option ={options}")
                options = int(input(ADMIN_CONSOLE))

        elif name in USERS:
            options = int(input(USER_CONSOLE))
            if options == 1:
                log.info(f'Entered Option=1 "Create User"')
                create_user(name)
            elif options == 2:
                log.info(f'Entered Option=2 "Update your record"')
                update_user_record(name)
            elif options == 3:
                log.info(f'Entered Option=3 "Check Your Details"')
                user_info(name)
            elif options == 4:
                log.info(f'Entered Option=4 "Read record"')
                read_records(name)

            elif options == 5:
                if restart(options):
                    restart_program()
                else:
                    exit()
            else:
                log.info(f'Entered wrong option={options}')
                print(f'Choosed wrong option ={options}')
                options = int(input(USER_CONSOLE))
        else:
            break


restart_program()
