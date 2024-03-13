import os

import pymysql
from dotenv import load_dotenv

from sql_utils import run_sql_file


class Database:
    def __init__(self):
        """
            Chargez les variables d'environnement de votre fichier .env, puis complétez les lignes 15 à 19 afin de récupérer les valeurs de ces variables
        """

        self.host =
        self.port =
        self.database =
        self.user =
        self.password =

        self._open_sql_connection()

        self.migration_counter = 0

    def _open_sql_connection(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )

        self.cursor = self.connection.cursor()

    def push_migration(self):
        migration_to_push = self.migration_counter + 1
        migration_file = f"db_scripts/migrate_{migration_to_push}.sql"

        run_sql_file(self.cursor, migration_file, accept_empty=False)
        self.migration_counter += 1

    def rollback(self):
        if self.migration_counter < 1:
            raise ValueError("There are no rollbacks in the rollback stack.")

        rollback_file = f"db_scripts/rollback_{self.migration_counter}.sql"

        run_sql_file(self.cursor, rollback_file)
        self.migration_counter -= 1

    def up(self):
        self.drop()
        run_sql_file(self.cursor, "db_scripts/up.sql")

    def drop(self):
        run_sql_file(self.cursor, "db_scripts/drop.sql")
        self.migration_counter = 0

    def get_table_names(self):
        req = f"SELECT table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_type = 'BASE TABLE' AND table_schema = '{self.database}';"
        self.cursor.execute(req)

        res = [x[0] for x in self.cursor.fetchall()]

        return res

    def get_table_column_names(self, table):
        req = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = '{self.database}' ORDER BY ORDINAL_POSITION;"
        self.cursor.execute(req)

        res = [x[0] for x in self.cursor.fetchall()]

        return res

    def get_table_data(self, table):
        req = f"SELECT * FROM {table};"
        self.cursor.execute(req)

        return [list(x) for x in self.cursor.fetchall()]

    def get_table_primary_key(self, table):
        req = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME = 'PRIMARY';"
        self.cursor.execute(req)

        return self.cursor.fetchone()

    def get_table_foreign_keys(self, table):
        req = f"SELECT COLUMN_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.database}' AND TABLE_NAME = '{table}' AND CONSTRAINT_NAME != 'PRIMARY';"
        self.cursor.execute(req)

        foreign_keys = []
        for foreign_key in self.cursor.fetchall():
            foreign_keys.append({
                "column_name": foreign_key[0],
                "referenced_table_name": foreign_key[1],
                "referenced_column_name": foreign_key[2]
            })

        return foreign_keys

    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.connection

    def get_migration_stack_size(self):
        return self.migration_counter
