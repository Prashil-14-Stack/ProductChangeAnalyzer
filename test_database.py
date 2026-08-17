from v2.database.connection import test_connection


if test_connection():

    print("PostgreSQL connection successful!")

else:

    print("PostgreSQL connection failed!")