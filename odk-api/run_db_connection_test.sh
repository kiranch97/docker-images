#!/bin/bash
pytest integration_tests/db_connection_test.py --sqlalchemy-connect-url=$DATABASE_CONNECTION_STRING