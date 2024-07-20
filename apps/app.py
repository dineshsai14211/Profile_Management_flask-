"""
This program manages a database of user records, allowing for the
addition, modification, partial updates, and deletion of records.
The records include details such as username,name, gender, date of birth, and company,dept.

"""
from flask import Flask, jsonify, request
from log.logging_logic import *
from emails.email_operations import *
from utilis.utility import *
from constants import *

app = Flask('__name__')


@app.route('/create_user')
def create_user():
    """
    These function is used to create user for Authentication and Authorisation
    :return: json
    """
    data = request.args
    name = data.get("name")
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
                    return jsonify(user_info)

            elif role == 'admin':
                user_info = create_user_info(role=role)
                if is_valid_record(user_info):
                    log.info(f"Admin {name} has created the admin user")
                    ALL_USERS.append(user_info["name"])
                    DATA["records"].append(user_info)
                    send_email([members for members in receivers],
                               RECORD_ADDED.format(name, user_info["name"], user_info))
                    print(f"New User={user_info["name"]} record added..")
                    return jsonify(user_info)
            else:
                raise ValueError(f"Incorrect role choosen - available options are normal and admin only")

        else:
            log.error(f"User={name} does not have create user profile permission")
            raise PermissionError(f"User {name} does not have create user profile permission")
    except ValueError as err:
        log.error(err)
        log.info(f'create_user function has ended...')
        return jsonify({"Error": str(err)}), 400

    except PermissionError as err:
        log.error(err)
        log.info(f'create_user function has ended...')
        return jsonify({"Error": str(err)}), 400

    except Exception as err:
        log.error(err)
        log.info(f'create_user function has ended...')
        return jsonify({"Error": str(err)}), 400


@app.route('/update_record')
def update_record():
    """
    This function update full records in DATA
    :return DATA: json
    """
    try:
        data = request.args
        Name = data.get("name")
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
                                       UPDATE_MESSAGE.format(Name, DATA["records"][item]))
                            log.info(f'updated record is = {DATA}')
                            return jsonify(DATA["records"][item])
        else:
            log.error(f'Entered user={Name} has no records')
            print(f'Entered user={Name} has no records')
            return jsonify({"Error": f"Entered user={Name} has no records"}), 400

    except ValueError as err:
        log.error(err)
        log.info(f'update_record function has ended...')
        return jsonify({"Error": str(err)}), 400

    except Exception as err:
        log.info(f'update_record function has ended...')
        log.error(err)
        return jsonify({"Error": str(err)}), 400
    log.info(f'update_record function has ended...')


@app.route('/update_user_record')
def update_user_record():
    """
    These function is used to update the user record for him.
    :return: json
    """
    try:
        data = request.args
        name = data.get("name")
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
                               UPDATE_USER_RECORD.format(name, DATA["records"][item]))
                    log.debug(f'Updated user={name} record = {DATA["records"][item]}')
                    return jsonify(DATA["records"][item])

    except ValueError as err:
        log.error(err)
        log.info(f"update_user_record function has ended....")
        return jsonify({"Error": str(err)}), 400

    except Exception as err:
        log.error(err)
        log.info(f"update_user_record function has ended....")
        return jsonify({"Error": str(err)}), 400

    log.info(f'update_user_record function has ended...')


@app.route('/partial_update_record')
def partial_update_record():
    """
    This function is used for partial update of records in DATA
    :return :  json
    """
    try:
        data = request.args
        Name = data.get("name")
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
                                   PARTIAL_UPDATE.format(Name, DATA["records"][item]))
                        log.info(f'"message:-" "Partial Modified "{Name}" record is ":-{DATA["records"][item]}')
                        return jsonify(DATA["records"][item])
        else:
            log.error(f'Entered user={Name} has no records')
            return jsonify({"Error": f"Entered user={Name} has no records"}), 400

    except Exception as err:
        log.error(err)
        log.info("partial_update_record function has ended...")
        return jsonify({"Error": str(err)}), 400

    log.info(f"Saved Record={DATA}")
    log.info("partial_update_record function has ended...")


@app.route('/reset_password')
def reset_password():
    """
    These function is used to reset the user password
    :return : json
    """
    log.info(f'reset_password function has started...')
    try:
        data = request.args
        Name = data.get("name")
        log.info(f'Admin enterd user name is "{Name}"')
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    Password = input(
                        "Enter the password that should contain one uppercase,lowercase,digit,special character = ")
                    log.info(f'Admin changed user={Name} password to "{Password}"')
                    if is_valid_password(Password):
                        log.debug(
                            f'Before the reset password User={Name} password is "{DATA['records'][item]['password']}"')
                        DATA["records"][item]["password"] = Password
                        send_email([members for members in receivers], RESET_PASSWORD.format(Name))
                        log.debug(
                            f'After the reset password User={Name} password is "{DATA['records'][item]['password']}"')
                        return jsonify({"password": DATA["records"][item]["password"]})
        else:
            log.warning(f"User={Name} record is not there")
            return jsonify({"Error": f"User={Name} record is not there"}), 400

    except Exception as err:
        log.error(err)
        log.info(f'reset_password function has ended...')
        return jsonify({"Error": str(err)}), 400
    log.info(f'reset_password function has ended...')


@app.route('/user_info')
def user_info():
    """
    These function is about checking user detailed information.
    if user is admin,can see any user information
    if normal user,can see only his information
    :return: dict
    """
    log.info(f'user_info function started...')
    try:
        data = request.args
        name = data.get("name")
        if name in ADMINS:
            Name = input("Enter the name of user to see his details:- ")
            log.info(f'Admin={name} has entered "{Name}" to see his information')
            if Name in ALL_USERS:
                for item in range(len(DATA["records"])):
                    if Name == DATA["records"][item]["name"]:
                        send_email([members for members in receivers],
                                   CHECK_USER_INFO.format(name, Name))
                        log.debug(f"User={Name} information :- {DATA["records"][item]}")
                        return jsonify(DATA["records"][item])
            else:
                log.error(f"User={Name},is not in records")
                raise Exception(f"User={Name},is not in records")

        if name in USERS:
            log.info(f"User={name} having checking his information")
            for item in range(len(DATA["records"])):
                if name == DATA["records"][item]["name"]:
                    send_email([members for members in receivers],
                               USER_INFO.format(name))
                    log.info(f"Your information :- {DATA["records"][item]}")
                    return jsonify(DATA["records"][item])

        else:
            raise Exception(f"User={name} record is not there")

    except Exception as err:
        log.error(err)
        log.info(f'user_info function ended...')
        return jsonify({"Error": str(err)}), 400

    log.info(f'user_info function ended...')


@app.route('/delete_record')
def delete_record():
    """
    This function will delete the record in DATA
    :return DATA:  dict
    """
    log.info(f'delete_record function has started...')
    try:
        data = request.args
        Name = data.get("name")
        if Name in ALL_USERS:
            for item in range(len(DATA["records"])):
                if Name == DATA["records"][item]["name"]:
                    del DATA["records"][item]
                    ALL_USERS.remove(Name)
                    send_email([members for members in receivers],
                               DELETE_MESSAGE.format(Name))
                    log.info(f'Deleted the {Name} record...')
                    return jsonify(DATA["records"][item])
                    break
        else:
            raise Exception(f'user {Name} is not there...')

    except Exception as err:
        log.error(err)
        log.info(f'delete_record function has ended....')
        return jsonify({"Error": str(err)}), 400

    log.info(f'delete_record function has ended....')


@app.route('/read_records')
def read_records():
    """
    These function is used to read the entire records
    :return: json
    """
    send_email([members for members in receivers], GET_ALL_MESSAGE)
    log.info(f'Saved Record = {DATA}')
    return jsonify(DATA)


app.run(debug=True)
