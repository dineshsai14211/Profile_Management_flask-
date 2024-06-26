"""
This program contains functions for validations of mobile number,name,dob,gender
"""
from app.constants import *
from datetime import datetime
import logging as log

log.basicConfig(filename="log/app.log", filemode="a", level=log.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s")


def is_excluded(mobile_num):
    """
    This function exclude the validation if mobile_num in EXCLUDED_NUMBERS
    :param mobile_num: int
    :return: bool
    """
    if mobile_num in EXCLUDED_NUMBERS:
        log.info(f"{mobile_num} in excluded list")
        log.info(f"Mobile number={mobile_num} verification is successful")
        print(f"Mobile number={mobile_num} verification is successful")
        return True
    return False


def is_valid_country(converted_str):
    """
    This function is for checking valid country code
    :param converted_str: str
    :return: bool
    """

    if converted_str[:2] in VALID_COUNTRY_LIST:
        log.info(f"Mobile number={converted_str} verification is successful")
        print(f"Mobile number={converted_str} verification is successful")
        return True
    else:
        log.error(f"Invalid country code - {converted_str[:2]}. Valid country codes are= {VALID_COUNTRY_LIST}")
        raise Exception(f"Error:-Invalid country code - {converted_str[:2]}. Valid country codes are= {VALID_COUNTRY_LIST}")


def is_mobile_length_valid(converted_str):
    """
    This function is for validating length of mobile number
    :param converted_str: str
    :return: bool
    """
    # Mobile length must be 12 digits

    if len(converted_str) == 12:
        return True
    else:
        log.error(f"Invalid Mobile number length {len(converted_str)}. Valid length is 12")
        raise Exception(f"Error:-Invalid Mobile number length {len(converted_str)}. Valid length is 12")


def is_valid_type(mobile):
    """
    This function is for checking type of mobile is int or not
    :param mobile: int
    :return: bool
    """
    if isinstance(mobile, int):
        return True
    else:
        log.error(f"Invalid mobile number type - {type(mobile)}")
        raise Exception(f"Error:-Invalid mobile number type - {type(mobile)}")


def is_valid_mobile(mobile):
    """
    This function is for validate the mobile number with different parameters
    :param mobile: int
    :return: bool
    """
    converted_str = str(mobile)
    mobile_num = int(converted_str[2:])
    if is_valid_type(mobile) and is_mobile_length_valid(converted_str):
        if is_excluded(mobile_num):
            return True
        if is_valid_country(converted_str):
            return True
    return False


def is_valid_name(name, mobile):
    """
    This function is for validating name that should contain only char,len>2,removing spaces
    :param name: str
    :param mobile: int
    :return: bool
    """
    name = name.replace(".", "").replace(" ", "").replace("_", "")
    if len(name) > 2:
        pass
    else:
        log.error(f"User name cannot be {len(name)} character for user mobile -{mobile}")
        raise ValueError(f"Error:-User name cannot be {len(name)} character for user mobile -{mobile}")

    if name.isalpha():
        pass
    else:
        log.error(f"User name {name} must be str only user mobile -{mobile}")
        raise ValueError(f"Error:-User name {name} must be str only user mobile -{mobile}")
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
        log.error(f'User={name},entered wrong format of DOB')
        raise ValueError(f'Error:-User={name},entered wrong format of DOB')


def is_valid_gender(gender, name):
    """
    This function is for validate the gender
    :param gender: str    :param name: str
    :return: bool
    """
    if gender in VALID_GENDER:
        return True
    else:
        log.error(f'User={name} entered invalid gender = {gender}')
        raise Exception(f'Error:-User={name} entered invalid gender = {gender}')


def is_valid_record(record):
    """
    This function is for validating a new record for inserting in to DATA
    :param record: dict
    :return: bool
    """
    if is_valid_mobile(record["mobile"]):
        if is_valid_name(record["name"], record["mobile"]):
            if is_valid_dob(record["dob"], record["name"]):
                if is_valid_gender(record["gender"], record["name"]):
                    return True
