""" This program will creates unit tests for the spendings_tracker file.

Driver/Navigator: Shelly Parra
Assignment: Final Project
Date: 12/09/2024

Challenges Encountered: Understanding unit testing.

"""


import csv
import sqlite3
import os
import pandas as pd
from spendings_tracker import Week
import spendings_tracker
import pytest


def test_init():
    # create a database connection and send it to the Week class
    conn = sqlite3.connect('week.db')
    week = Week(conn)
    
    cq = "SELECT tableName FROM sqlite_master WHERE type = 'table' AND tableName = 'week'"
    week.cursor.execute(cq)
    table_info = week.cursor.fetchall()
    
    assert table_info != [], "Table does not exist."


if __name__ == "__main__":
    test_init()