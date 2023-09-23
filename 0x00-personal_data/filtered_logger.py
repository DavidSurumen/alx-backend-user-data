#!/usr/bin/env python3
"""
Filtered logger module
"""
import logging
import re
from typing import List


patterns = {
        'extract': lambda fields, separator: r'(?P<field>{})=[^{}]*'.
        format('|'.join(fields), separator),
        'replace': lambda redaction: r'\g<field>={}'.format(redaction),
        }


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Filters a log file
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


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
