"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as mobile number, name, gender, date of birth, and company.

"""
from constants import *
from utilis.utility import *


def create_user(name, role=None):
    """
    These function is used to create user for Authentication and Authorisation
    :param name: str    :param role: str
    :return: bool
    """
    try:
        if not authenticate_user(name):
            log.warning(f"Unauthorized User={name}, trying to access the application...")
            raise Exception(f"UnAuthorised user {name} trying to access the application")

        # Authorisation
        if name in ADMINS:
            log.info(f"User {name} admin authorization is successfull")
            print(f"Enter role normal user or admin user ?:")
            role = input(f"Options are normal, admin:")

            if role == 'normal':
                user_info = create_user_info(role=role)
                USERS.append(user_info["username"])
                USERS_DETAILS.append(user_info)
                print(f"{user_info['username']} added as a normal user")
            elif role == 'admin':
                user_info = create_user_info(role=role)
                ADMINS.append(user_info["username"])
                ADMIN_DETAILS.append(user_info)
                print(f"{user_info['username']} added as a admin user")
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


# POST
def create_new_record(record):
    """
    This is function is for inserting new record
    :param record: dict
    :return: DATA : dict
    """
    log.info(f'create_new_record function started...')
    try:
        if isinstance(record, dict):
            if "mobile" in record:
                log.info(f'{record["mobile"]} --> create_new_record function started...')
                if is_valid_record(record):
                    REGISTERED_NUMBERS.append(record["mobile"])
                    DATA["records"].append(record)
                    log.info(f'Record added successfully :- {DATA}')
                    return f'Saved record for {record["mobile"]} is = {DATA}'
            else:
                log.error(f'In dict record the key "mobile" is not there')
                raise Exception(f'In dict record the key "mobile" is not there')
        else:
            log.error(f'The entered DATA records is not in format dict,it is in {type(record)}')
            raise Exception(f'The entered DATA records is not in format dict,it is in {type(record)}')
    except Exception as err:
        print(err)
    log.info(f'{record["mobile"]} --> create_new_record function ended...')


log.info(f'Saved records = {DATA}')


# PUT
def update_record(DATA):
    """
    This function update full records in DATA
    :param DATA: dict    :return DATA: dict
    """
    try:
        for item in range(len(DATA["records"])):
            log.info(f'{DATA["records"][item]["mobile"]} --> update_record function has started...')
            current_record = DATA["records"][item]
            mobile = current_record["mobile"]
            company = current_record["company"]
            log.info(f'"message:-Modifying {item + 1} record"')
            print(f'Updating {item + 1} record:-')

            Name = input(f"Enter name for {item + 1} record:- ")
            Gender = input(f'Enter the gender for {item + 1} record:-')
            Company = input(f"Enter company name for {item + 1} record:- ")
            log.info(f'"message:- Previous record of {item + 1} is :-" {DATA["records"][item]}')

            if is_valid_name(Name, mobile):
                if is_valid_gender(Gender, Name):
                    current_record["name"] = Name
                    current_record["gender"] = Gender
                    current_record["company"] = Company
                    log.info(f'"message:-" "Modified {item + 1} record is ":-{DATA["records"][item]}')
                    log.info(f'updated record is = {DATA}')
    except ValueError as err:
        print(err)

    except Exception as err:
        print(err)
    log.info(f'update_record function has ended...')
    return DATA


# PATCH
def partial_update_record(DATA):
    """
    This function is used for partial update of records in DATA
    :param DATA: dict    :return DATA:  dict
    """
    try:
        for item in range(len(DATA["records"])):
            log.info(f'{DATA["records"][item]["mobile"]} --> partial_update_record function has started...')
            log.info(f'"message:-" "Partial Modifying {item + 1} record"')
            print(f'Partially updating {item + 1} record:-')

            Name = input(f"Enter name for {item + 1} record:- ")
            if is_valid_name(Name, DATA["records"][item]["mobile"]):
                DATA["records"][item]["name"] = Name

            log.info(f'"message:-" "Partial Modified {item + 1} record is ":-{DATA["records"][item]}')
    except Exception as err:
        print(err)
    log.info(f"Saved Record={DATA}")
    log.info("partial_update_record function has ended...")
    return f"partially updated saved record are={DATA}"


# DELETE
def delete_record(DATA):
    """
    This function will delete the record in DATA
    :param DATA: dict    :return DATA:  dict
    """
    log.info(f'delete_record function has started...')
    try:
        mobile = input("Enter mobile number of which record to delete:-")
        if not mobile.isdigit():
            log.error(f"User={name} entered incorrect format for mobile={type(mobile)}")
            raise ValueError(f"User={name} entered incorrect format for mobile={type(mobile)}")

        for item in range(len(DATA["records"])):
            if int(mobile) in REGISTERED_NUMBERS:
                if int(mobile) == DATA["records"][item]["mobile"]:
                    DATA["records"][item].clear()
                    log.info(f'Deleted the record contains mobile number={mobile}')
                    log.info(f'After deleting data is = {DATA}')
            else:
                log.debug(f'Entered number is not a registered number')
                return f'Entered number is not a registered number'
        return f'After deleting= {DATA}'
    except ValueError as err:
        print(err)


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
    print(f"Unauthorized User={name}, trying to access the application...")
    exit()

while True:
    if name in ADMINS:
        options = int(input(
            f"Which Operation you need to perform \n1)Create User \n2)Create New_record \n3)Update Record \n4)Partially Update Record \n5)Delete Record \n6)Read Records \n7)Exit \n Choose from above option:- "))
        if options == 1:
            log.info(f'Entered Option=1 "Create User"')
            create_user(name)
        elif options == 2:
            log.info(f'Entered Option=2 "Create New_record"')
            print(create_new_record(
                {"mobile": 454234234245, "name": "kumar", "gender": "M", "dob": "21-2-2001", "company": "KXN"}))
            print(create_new_record(
                {"mobile": 919000070128, "name": "Kajal", "gender": "F", "dob": "2001-2-2", "company": "APD"}))
        elif options == 3:
            log.info(f'Entered Option=3 "Update Record"')
            print("Updated Records are=", update_record(DATA))
        elif options == 4:
            log.info(f'Entered Option=4 "Partially Update Record"')
            print(partial_update_record(DATA))
        elif options == 5:
            log.info(f'Entered Option=5 "Delete Record"')
            print(delete_record(DATA))
        elif options == 6:
            log.info(f'Entered Option=6 "Read Record"')
            read_records()
        elif options == 7:
            log.info(f'Entered Option=7 Exited..')
            cond = False
            break
        else:
            log.info(f'Entered wrong Option={options}')
            print(f"Choosed wrong option ={options}")
            options = int(input(
                f"Which Operation you need to perform \n1)create_user \n2)create_new_record \n3)update_record \n4)partial_update_record \n5)delete_record \n6)read_records 7)Exit \n Choose from above option:- "))

    elif name in USERS:
        options = int(input(f'Which operation need to perform \n1)Create User \n2)Read Records \n3)Exit \n Choose from above options :- '))
        if options == 1:
            log.info(f'Entered Option=1 "Create User"')
            create_user(name)
        elif options == 2:
            log.info(f'Entered Option=2 "Read Record"')
            read_records()
        elif options == 3:
            log.info(f'Entered Option=3 "Exited"')
            break
        else:
            log.info(f'Entered wrong option={options}')
            print(f'Choosed wrong option ={options}')
            options = int(input(
                f'Which operation need to perform \n1)create_user 2)read_records 3)Exit \n Choose from above options :- '))
    else:
        break
