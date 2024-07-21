"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as username,name, gender, date of birth, and company,dept.
"""

# Importing 3rd party packages
from flask import Flask, jsonify, request

# Importing local packages
from log.logging_logic import *
from emails.email_operations import *
from utilis.utility import *
import constants as const
from constants import *
from custom_exceptions.exceptions import *

# Creating application instance
app = Flask('__name__')


@app.route('/create_user', methods=["POST"])
def create_user():
    """
    These function is used to create user for Authentication and Authorisation purpose.
    :return: json
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - create_user function has started...')

    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            role = input(f"Which role,normal(or)admin: ")

            if role == const.NORMAL:
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.debug(f'{name} - Admin has created the normal user')
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)

                    send_email([members for members in receivers],
                               RECORD_ADDED.format(name, user_info["name"], user_info))
                    log.debug(f"{name} - '{user_info["name"]}' Normal user record added..")
                    return jsonify(message=user_info["name"] + " record has been created", admin=False,
                                   status=const.SUCCESS), 200

            elif role == const.ADMIN:
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.debug(f"{name} - Admin has created the admin user")
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)

                    send_email([members for members in receivers],
                               RECORD_ADDED.format(name, user_info["name"], user_info))
                    log.debug(f"{name} - {user_info["name"]} admin user record added..")
                    return jsonify(message=user_info["name"] + " record has been created", admin=True,
                                   status=const.SUCCESS), 200
            else:
                raise ValueError(f"{name} - Incorrect role choosen - available options are normal and admin only")

        else:
            log.error(f"{name} - does not have create user profile permission")
            raise AuthorizationError(f"{name} - does not have create user profile permission")
    except ValueError as val_err:
        log.error(val_err)
        return jsonify(error=str(val_err), status=const.FAILED), 400

    except AuthorizationError as authz_err:
        log.error(authz_err)
        return jsonify(error=str(authz_err), status=const.FAILED), 403

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - create_user function has ended...')


@app.route('/update_record', methods=["PUT"])
def update_record():
    """
    This function is used to update full record of a user in DATA
    :return DATA: json
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - update_record function has started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            Name = input("Enter the name of the user, to update his record = ")
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    current_record = DATA["records"][item]
                    if Name == current_record["name"]:

                        log.debug(f'{name} - "Modifying User={Name} record"')
                        log.debug(f'{name} - "Previous record of User={Name}  is :-" {DATA["records"][item]}')

                        Username = input(f"Enter the username for User={Name}  record :- ")
                        Name = input(f"Enter name for User={Name}  record:- ")
                        Gender = input(f'Enter the gender for User={Name}  record:-')
                        Dept = input(f'Enter your Depeartment fro User={Name}  record:-')

                        if is_valid_name(Name):
                            if is_valid_gender(Gender, Name):
                                current_record["username"] = Username
                                current_record["name"] = Name
                                ALL_USERS.append(Name)
                                current_record["gender"] = Gender
                                current_record["dept"] = Dept

                                log.debug(f'{name} - "Modified User={Name}  record is ":-{DATA["records"][item]}')
                                send_email([members for members in receivers],
                                           UPDATE_MESSAGE.format(Name, DATA["records"][item]))
                                return jsonify(message=DATA["records"][item]["name"] + " record has been updated",
                                               admin=DATA["records"][item]["isadmin"], status=const.SUCCESS), 200
            else:
                log.error(f'{name} - user={Name} has no records,check name once')
                return jsonify(error=f'{Name} has no records,check name once', status=const.FAILED), 400
        else:
            log.error(f"{name} - does not have update user permission")
            raise AuthorizationError(f"{name} - does not have update user permission")

    except ValueError as val_err:
        log.error(f"{name} - {val_err}")
        return jsonify(error=str(val_err), status=const.FAILED), 400

    except AuthorizationError as authz_err:
        log.error(authz_err)
        return jsonify(error=str(authz_err), status=const.FAILED), 403

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - update_record function has ended...')


@app.route('/update_user_record', methods=["PUT"])
def update_user_record():
    """
    These function is used to update the records of individuals.
    :return: json
    """
    data = request.args
    name = data.get("name")
    log.info(f"{name} - update_user_record function has started....")
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        for item in range(len(DATA["records"])):
            if name == DATA["records"][item]["name"]:
                log.debug(f'{name} - has updating his record')

                current_record = DATA["records"][item]
                Username = input(f"Enter the username for {item + 1} record :- ")
                Gender = input(f'Enter the gender for {item + 1} record:-')
                Dept = input(f'Enter your Department for {item + 1} record:-')

                log.debug(f'{name} - Before updating the record is= {current_record}')

                if is_valid_gender(Gender, name):
                    current_record["username"] = Username
                    current_record["gender"] = Gender
                    current_record["dept"] = Dept
                    log.debug(f'{name} - After user updated his record = {current_record}')
                    send_email([members for members in receivers],
                               UPDATE_USER_RECORD.format(name, DATA["records"][item]))
                    return jsonify(message=DATA["records"][item]["name"] + " has updated his record",
                                   admin=DATA["records"][item]["isadmin"], status=const.SUCCESS), 200

    except ValueError as val_err:
        log.error(f"{name} - {val_err}")
        return jsonify(error=str(val_err), status=const.FAILED), 400

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - update_user_record function has ended...')


@app.route('/partial_update_record', methods=["PATCH"])
def partial_update_record():
    """
    This function is used to partial update of records in DATA
    :return : json
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - partial_update_record has started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            Name = input("Enter the name of user, to partially update his record = ")
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        log.debug(f'{name} - Partial Modifying "{Name}" record')

                        Name = input(f'Enter name for "{Name}" record:- ')
                        if is_valid_name(Name):
                            DATA["records"][item]["name"] = Name
                            ALL_USERS.append(Name)
                            send_email([members for members in receivers],
                                       PARTIAL_UPDATE.format(Name, DATA["records"][item]))
                            log.debug(f'{name} - Partial Modified "{Name}" record is :-{DATA["records"][item]}')
                            return jsonify(message=DATA["records"][item]["name"] + " partially updated the record",
                                           admin=DATA["records"][item]["isadmin"], status=const.SUCCESS), 200
            else:
                log.error(f'{name} - user={Name} has no records,check name once')
                return jsonify(error=f'{Name} has no records,check name once', status=const.FAILED), 400
        else:
            log.error(f"{name} - does not have partially update record permission")
            raise AuthorizationError(f"{name} - does not have partially update record permission")

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except AuthorizationError as authz_err:
        log.error(authz_err)
        return jsonify(error=str(authz_err), status=const.FAILED), 403

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500

    finally:
        log.info(f"{name} - partial_update_record function has ended...")


@app.route('/reset_password', methods=["PATCH"])
def reset_password():
    """
    These function is used to reset the user password.
    :return : json
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - reset_password function has started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            Name = input("Enter the name of the user, to reset his password = ")
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        Password = input(
                            "Enter the password that should contain one uppercase,lowercase,digit,special character = ")
                        user_name = Name
                        if is_valid_password(Password):
                            log.debug(
                                f'{name} - Before the reset password User={Name} password is "{DATA['records'][item]['password']}"')
                            DATA["records"][item]["password"] = Password
                            send_email([members for members in receivers], RESET_PASSWORD.format(Name))
                            log.debug(
                                f'{name} - After the reset password User={Name} password is "{DATA['records'][item]['password']}"')

                            return jsonify(message=user_name + " password has been updated", status=const.SUCCESS), 200
            else:
                log.error(f'{name} - user={Name} has no records,check name once')
                return jsonify(error=f'{Name} has no records,check name once', status=const.FAILED), 400
        else:
            log.error(f"{name} - does not have reset password permission")
            raise AuthorizationError(f"{name} - does not have reset password permission")

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except AuthorizationError as authz_err:
        log.error(authz_err)
        return jsonify(error=str(authz_err), status=const.FAILED), 403

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - reset_password function has ended...')


@app.route('/user_info', methods=["GET"])
def user_info():
    """
    These function is about checking user detailed information.
    if user is admin,can see any user information
    if normal user,can see only his information
    :return: dict
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - user_info function started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            Name = input("Enter the name of user to see his details:- ")
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        send_email([members for members in receivers],
                                   CHECK_USER_INFO.format(name, Name))
                        log.debug(f"{name} - User={Name} information :- {DATA["records"][item]}")
                        return jsonify(record=DATA["records"][item], status=const.SUCCESS), 200
            else:
                log.error(f"{name} - {Name},is not in records,check name once")
                raise Exception(f"{name} - {Name},is not in records,check name once")

        if name in USERS:
            for item in range(len(DATA["records"])):
                if name == DATA["records"][item]["name"]:
                    send_email([members for members in receivers],
                               USER_INFO.format(name))
                    log.debug(f"{name} - Information :- {DATA["records"][item]}")
                    return jsonify(record=DATA["records"][item], status=const.SUCCESS), 200

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500

    finally:
        log.info(f'{name} - user_info function ended...')


@app.route('/delete_record', methods=["DELETE"])
def delete_record():
    """
    This function will delete the record in DATA
    :return DATA:  dict
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - delete_record function has started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        if name in ADMINS:
            Name = input("Enter the name of user, to delete his record = ")
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        del DATA["records"][item]
                        ALL_USERS.remove(Name)
                        send_email([members for members in receivers],
                                   DELETE_MESSAGE.format(Name))
                        log.debug(f'{name} - Deleted the {Name} record...')
                        return jsonify(message=Name + " record has been deleted", status=const.SUCCESS), 200
            else:
                log.error(f"{name} - {Name},is not in records,check name once")
                raise Exception(f"{name} - {Name},is not in records,check name once")
        else:
            log.error(f"{name} - does not have delete record permission")
            raise AuthorizationError(f"{name} - does not have delete record permission")

    except AuthorizationError as authz_err:
        log.error(authz_err)
        return jsonify(error=str(authz_err), status=const.FAILED), 403

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - delete_record function has ended....')


@app.route('/read_records', methods=["GET"])
def read_records():
    """
    These function is used to read the entire records
    :return: json
    """
    data = request.args
    name = data.get("name")
    log.info(f'{name} - read_records function has started...')
    try:
        if not authenticate_user(name):
            raise AuthenticationError(f"Unauthorised user= {name} detected..")

        send_email([members for members in receivers], GET_ALL_MESSAGE)
        return jsonify(message=DATA, status=const.SUCCESS), 200

    except AuthenticationError as auth_err:
        log.error(auth_err)
        return jsonify(error=str(auth_err), status=const.FAILED), 401

    except Exception as err:
        log.error(f"{name} - {err}")
        return jsonify(error=str(err), status=const.FAILED), 500
    finally:
        log.info(f'{name} - read_records function has ended...')


# Run the application
app.run(debug=True)
