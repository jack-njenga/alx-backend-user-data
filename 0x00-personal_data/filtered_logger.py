#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log
message obfuscated:
"""
import re
import logging
import os
import mysql.connector as connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: list,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated:
    """
    log_msg = message
    for field in fields:
        log_msg = re.sub(r'{}=[^{}]+{}'.
                         format(field, separator, separator),
                         f"{field}={redaction}{separator}", log_msg)
    return log_msg


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    fields = None

    def __init__(self, fields: list):
        """init"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """str format"""
        msg = super(RedactingFormatter, self).format(record)
        red_msg = filter_datum(self.fields, self.REDACTION,
                               msg, self.SEPARATOR)

        return red_msg


def get_logger():
    """takes no arguments and returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db():
    """returns a db connection"""

    db = os.environ.get('PERSONAL_DATA_DB_NAME')
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')

    connection = connector.connect(
        password=pwd,
        db=db,
        host=host,
        user=user,
    )
    return connection


def main() -> None:
    """main"""
    query = """SELECT name, email, phone, ssn, password, ip,
                last_login, user_agent from users;"""

    db = get_db()
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    for row in cursor.fetchall():
        (name, email, phone, ssn, password, ip, last_login, user_agent) = row
        fmt1 = "[HOLBERTON] user_data INFO: name=***; "
        fmt2 = "email=***; phone=***; ssn=***; password=***; "
        fmt3 = f"ip={ip}; last_login={last_login}; user_agent={user_agent}"
        print(f"{fmt1}{fmt2}{fmt3}")
    cursor.close()
    db.close()
    return None


if __name__ == "__main__":
    main()
