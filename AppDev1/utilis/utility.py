from app.constants import *
from datetime import datetime
import logging as log

log.basicConfig(filename="log/app.log", filemode="a", level=log.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s")


def is_valid_name(name):
    """
    This function is for validating name that should contain only char,len>2,removing spaces
    :param name: str
    :return: bool
    """
    name = name.replace(".","").replace(" ", "").replace("_", "")
    if len(name) > 2:
        pass
    else:
        log.error(f"User name cannot be {len(name)} character")
        raise ValueError(f"Error:-User name cannot be {len(name)} character")

    if name.isalpha():
        pass
    else:
        log.error(f"User name {name} must be str only user ")
        raise ValueError(f"Error:-User name {name} must be str only")
    return True


def is_valid_dob(dob, name):
    """
    This function validate the DOB in format="%Y-%m-%d"
    :param dob: str
    :param name: name
    :return: bool
    """
    Format = "%Y-%m-%d"
    try:
        res = datetime.strptime(dob, Format)
        return True
    except ValueError:
        log.error(f'User={name},has wrong format of DOB')
        raise ValueError(f'Error:-User={name},has wrong format of DOB')


def is_valid_gender(gender, name):
    """
    This function is for validate the gender
    :param gender: str    :param name: str
    :return: bool
    """
    if gender in VALID_GENDER:
        return True
    else:
        log.error(f'User={name} has invalid gender = {gender}')
        raise Exception(f'Error:-User={name} has invalid gender = {gender}')


def is_valid_record(record):
    """
    This function is for validating a new record for inserting in to DATA
    :param record: dict
    :return: bool
    """

    if is_valid_name(record["name"]):
        if is_valid_dob(record["dob"], record["name"]):
            if is_valid_gender(record["gender"], record["name"]):
                return True


def authenticate_user(name):
    """

    :param name:
    :return:
    """
    if name in USERS or name in ADMINS:
        log.info(f"User={name} authentication successfull")
        print(f"User {name} authenticated successfully - meaning basic info verified ")
        return True
    return False


def create_user_info(role):
    global admin
    user = input(f"Enter username:")
    name = input(f"Enter Name:")
    initial = input(f"Enter first character of surname:")
    dept = input(f"Enter the department:")
    dob = input(f"Enter the DOB:")
    gender = input(f"Enter the gender:")
    if role == "normal":
        admin = False
    elif role == "admin":
        admin = True
    return {"username": user, "name": name + "." + initial, "dept": dept, "dob": dob, "gender": gender,
            "isadmin": admin}
