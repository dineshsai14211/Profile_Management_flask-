"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as mobile number, name, gender, date of birth, and company.

"""

from constants import *
from utilis.utility import *


# POST
def new_record(record):
    """
    This is function is for inserting new record
    :param record: dict
    :return: DATA : dict
    """
    log.info(f'new_record function started...')
    try:
        if isinstance(record, dict):
            if "mobile" in record:
                log.info(f'{record["mobile"]} --> new_record function started...')
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
    log.info(f'{record["mobile"]} --> new_record function ended...')


print(new_record({"mobile": 454234234245, "name": "kumar", "gender": "M", "dob": "21-2-2001", "company": "KXN"}))
# GET
print(new_record({"mobile": 919000070128, "name": "Kajal", "gender": "F", "dob": "2001-2-2", "company": "APD"}))
# GET
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
            print(f'Updating {item+1} record:-')

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


print("Updated Records are=", update_record(DATA))


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
            print(f'Partially updating {item+1} record:-')

            Name = input(f"Enter name for {item + 1} record:- ")
            if is_valid_name(Name, DATA["records"][item]["mobile"]):
                DATA["records"][item]["name"] = Name

            log.info(f'"message:-" "Partial Modified {item + 1} record is ":-{DATA["records"][item]}')
    except Exception as err:
        print(err)
    log.info(f"Saved Record={DATA}")
    log.info("partial_update_record function has ended...")
    return f"partially updated saved record are={DATA}"


print(partial_update_record(DATA))


# DELETE
def delete_record(DATA):
    """
    This function will delete the record in DATA
    :param DATA: dict    :return DATA:  dict
    """

    mobile = int(input("Enter mobile number of which record to delete:-"))
    log.info(f'{mobile} --> delete_record function has started...')

    for item in range(len(DATA["records"])):
        if mobile in REGISTERED_NUMBERS:
            if mobile == DATA["records"][item]["mobile"]:
                DATA["records"][item].clear()
        else:
            log.debug(f'Entered number is not a registered number')
            return f'Entered number is not a registered number'

    log.info(f'Deleted the record contains mobile number={mobile}')
    log.info(f'After deleting data is = {DATA}')
    return f'After deleting= {DATA}'


print(delete_record(DATA))

print(f'After performing all HTTP methods, Saved records is = {DATA}')
