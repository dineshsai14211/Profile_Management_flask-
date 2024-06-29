# email configurations
SMTP_PORT = 587  # For starttls
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "dineshsai14211@gmail.com"
RECEIVER_EMAIL = ["dineshsai14211@gmail.com", "danepaku@gitam.in"]
PASSWORD = "izdlrkcuyzrlwxec"

DELETE_MESSAGE = """
Hlo Team
Admin has deleted the Record in DATA,performed DELETE Method
Thank you 
"""
UPDATE_MESSAGE = """
Hlo team
Admin has updated the records in DATA,it'means Performed PUT Method
Thank You
"""
GET_ALL_MESSAGE = """
Some one is checking all users information from the table
"""
PARTIAL_UPDATE = """
Hlo Team
Admin has partially updated the records in DATA, It's means performed PATCH Method
Thank you
"""
CREATE_USER = """
Hlo team
Admin has triggered the create_user function to crate user(or)admin
Check logs for better understand
"""
UNAUTHENTICATED_MESSAGE = f"""
Hlo team
ALERT:-Unauthenticated user, trying to access the application
check logs
"""


# print("This is smtp_port---", SMTP_PORT)
# print("This is email_password", PASSWORD)
