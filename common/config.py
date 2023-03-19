import logging
import mysql.connector
import subprocess
from locust import events
import os


database_name: str = "book_library"
host_db: str = "localhost"
user_db: str = os.environ.get("USER")
password_db: str = os.environ.get("PASSWORD")
path_to_mysql_dump: str = os.environ.get("PATHTOMYSQLDUMP")
path_to_mysql: str = os.environ.get("PATHTOMYSQL")
# run script in root directory.
dump_file: str = "data_base_backup/database_dump.sql"

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logging.getLogger(__name__).setLevel("INFO")
    print("A new test is ending")
    # dump test database state before tests
    process = subprocess.Popen([path_to_mysql_dump, f"--user={user_db}", f"--password={password_db}",
                                f"--host={host_db}", f"{database_name}",
                                f"--result-file={dump_file}"])
    process.wait()
    logging.info("Start test")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Restore the state of the database given from before load testing
    auth_plugin must be mysql_native_password ,in mySQL 8.0
    caching_sha2_password is the default authentication plugin rather than
    """
    logging.info("Stopping test")
    mydb = mysql.connector.connect(
        buffered=True,
        host=host_db,
        user=user_db,
        password=password_db
    )

    mycursor = mydb.cursor()
    mycursor.execute(f"drop database {database_name}")
    mydb.commit()

    mycursor.execute(f"create database {database_name}")
    mydb.commit()
    mydb.close()

    subprocess.run(
        f"{path_to_mysql} --user={user_db} --password={password_db} --host={host_db} {database_name}"
        + f" < {dump_file}", shell=True)
    logging.info("Test is stop")