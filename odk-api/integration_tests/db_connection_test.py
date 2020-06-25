import pytest
from pytest_sqlalchemy import connection
from odklib.DatabaseManager import DatabaseManager

# first checking for basic connection
def test_connection(connection):
    assert connection

# then checking the DatabaseManager class with same connection
def test_database_manager(connection):
    db_manager = DatabaseManager(connection.engine.url)

    assert db_manager.has_connection == True