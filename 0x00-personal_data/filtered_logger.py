#!/usr/bin/env python3
"""
Filtered logger module
"""
import logging
import re
from typing import List
import mysql.connector
import os


patterns = {
        'extract': lambda fields, separator: r'(?P<field>{})=[^{}]*'.
        format('|'.join(fields), separator),
        'replace': lambda redaction: r'\g<field>={}'.format(redaction),
        }


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filters a log file
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """
    Creates a new logger for user data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Creates a connector to a secure mysql database
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_passw = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    conn = mysql.connector.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_passw,
            db=db_name,
            )
    return conn


def main() -> None:
    """
    Logs information about a user
    """
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    cols = fields.split(',')
    query = "SELECT {} FROM users;".format(fields)
    logger = get_logger()
    conn = get_db()

    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(cols, row),
                    )
            msg = '{};'.format('; '.join(list(record)))
            args = ('user_data', logging.INFO, None, None, msg, None, None)
            log = logging.LogRecord(*args)
            logger.handle(log)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a LogRecord.
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


if __name__ == '__main__':
    main()
