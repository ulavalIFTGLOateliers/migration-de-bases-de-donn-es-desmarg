import os
import sys
from collections import OrderedDict

from database import Database
from grading_utils import failable, load_db_states_from_json


class Grader:
    def __init__(self):
        """
            Cette interface sert à corriger les soumissions des étudiants.

            Il est possible d'ajouter autant de tests que désiré, ainsi que modifier les tests existants
            Tous les tests doivent être ajoutés au dictionnaire self.grading_template, dans la section correspondante parmis:
                - prereq
                - up
                - after_migration_1
                - after_rollback_1
                - after_migration_2
                - after_rollback_2

            ATTENTION: les sections migration_1, rollback_1, migration_2 et rollback_2 ne peuvent PAS être modifiées, sauf leur nombre de points respectif.

            Chaque entrée de ce dictionnaire doit être de la forme:

                    "[nom du test]": {
                        "callable": callable,    # fonction de test retournant un booléen
                        "points": int,           # nombre de points
                        "passed": Bool           # statut de réussite du test | False par défaut
                    }
        """

        self.grading_template = OrderedDict({
            # "prereq": {
            #     "idul": {
            #         "callable": self._idul,
            #         "points": 1,
            #         "passed": False
            #     }
            # },
            "up": {
                "connexion": {
                    "callable": self._up,
                    "points": 1,
                    "passed": False
                }
            },
            "migration_1": {
                "migration 1": {
                    "callable": self._migration_1,
                    "points": 1,
                    "passed": False
                }
            },
            "after_migration_1": {
                "schema des tables": {
                    "callable": self._check_state_schema("after_migration_1"),
                    "points": 1,
                    "passed": False
                },
                "contenu des tables": {
                    "callable": self._check_state_content("after_migration_1"),
                    "points": 1,
                    "passed": False
                },
                "clés": {
                    "callable": self._check_state_keys("after_migration_1"),
                    "points": 1,
                    "passed": False
                }
            },
            "rollback_1": {
                "rollback 1": {
                    "callable": self._rollback_1,
                    "points": 1,
                    "passed": False
                }
            },
            "after_rollback_1": {
                "schema des tables": {
                    "callable": self._check_state_schema("initial_state"),
                    "points": 1,
                    "passed": False
                },
                "contenu des tables": {
                    "callable": self._check_state_content("initial_state"),
                    "points": 1,
                    "passed": False
                },
                "clés": {
                    "callable": self._check_state_keys("initial_state"),
                    "points": 1,
                    "passed": False
                }
            },
            # "migration_2": {
            #     "migration 2": {
            #         "callable": self._migration_2,
            #         "points": 1,
            #         "passed": False
            #     }
            # },
            # "after_migration_2": {
            #     "schema des tables": {
            #         "callable": self._check_state_schema("after_migration_2"),
            #         "points": 1,
            #         "passed": False
            #     },
            #     "contenu des tables": {
            #         "callable": self._check_state_content("after_migration_2"),
            #         "points": 1,
            #         "passed": False
            #     },
            #     "clés": {
            #         "callable": self._check_state_keys("after_migration_2"),
            #         "points": 1,
            #         "passed": False
            #     }
            # },
            # "rollback_2": {
            #     "rollback 2": {
            #         "callable": self._rollback_2,
            #         "points": 1,
            #         "passed": False
            #     }
            # },
            # "after_rollback_2": {
            #     "schema des tables": {
            #         "callable": self._check_state_schema("after_migration_1"),
            #         "points": 1,
            #         "passed": False
            #     },
            #     "contenu des tables": {
            #         "callable": self._check_state_content("after_migration_1"),
            #         "points": 1,
            #         "passed": False
            #     },
            #     "clés": {
            #         "callable": self._check_state_keys("after_migration_1"),
            #         "points": 1,
            #         "passed": False
            #     }
            # }
        })

        self.target_states = load_db_states_from_json()

    def run(self):
        """
        Logique de correction.
        Roules les tests dans l'ordre d'exécution classique.
        Ne devrait pas être modifié, sauf si d'autres étapes s'ajoutent
        """

        # self._run_section_tests("prereq")
        # if not self.grading_template["prereq"]["idul"]["passed"]:
        #     return

        self._run_section_tests("up")
        if not self.grading_template["up"]["connexion"]["passed"]:
            return

        self._run_section_tests("migration_1")
        if not self.grading_template["migration_1"]["migration 1"]["passed"]:
            return

        self._run_section_tests("after_migration_1")

        self._run_section_tests("rollback_1")
        if not self.grading_template["rollback_1"]["rollback 1"]["passed"]:
            return

        self._run_section_tests("after_rollback_1")

        # self._run_section_tests("migration_2")
        # if not self.grading_template["migration_2"]["migration 2"]["passed"]:
        #     return

        # self._run_section_tests("after_migration_2")

        # self._run_section_tests("rollback_2")
        # if not self.grading_template["rollback_2"]["rollback 2"]["passed"]:
        #     return

        # self._run_section_tests("after_rollback_2")

    @failable
    def _idul(self):
        return os.stat("idul.txt").st_size > 0

    @failable
    def _up(self):
        """
        Lance la BD de l'étudiant, puis effectue un ping.
        :return: True si la connexion fonctionne, False sinon
        """
        self.database = Database()
        self.cursor = self.database.get_cursor()
        self.database.get_connection().ping(reconnect=False)
        self.database.up()
        return True

    @failable
    def _migration_1(self):
        """
        Effectue la première migration
        :return: True si la migration ne lance pas d'erreur, False sinon
        """
        self.database.push_migration()
        return True

    @failable
    def _rollback_1(self):
        """
        Effectue la première migration arrière
        :return: True si le rollback ne lance pas d'erreur, False sinon
        """
        self.database.rollback()
        return True

    @failable
    def _migration_2(self):
        """
        Effectue la deuxième migration
        :return: True si la migration ne lance pas d'erreur, False sinon
        """
        for i in range(self.database.get_migration_stack_size(), 2):
            self.database.push_migration()
        return True

    @failable
    def _rollback_2(self):
        """
        Effectue la deuxième migration arrière
        :return: True si la migration ne lance pas d'erreur, False sinon
        """
        self.database.rollback()
        return True

    def _run_section_tests(self, section):
        for test_attributes in self.grading_template[section].values():
            test_attributes["passed"] = test_attributes["callable"]()

    def _check_state_schema(self, state):
        @failable
        def wrapper():
            target_tables_schema = self.target_states[state]["tables"]
            target_table_names = target_tables_schema.keys()
            actual_table_names = self.database.get_table_names()

            if sorted(target_table_names) != sorted(actual_table_names):
                return False

            for target_table in target_table_names:
                target_table_columns = target_tables_schema[target_table]["columns"]
                actual_table_columns = self.database.get_table_column_names(target_table)
                if sorted(target_table_columns) != sorted(actual_table_columns):
                    return False

            return True

        return wrapper

    def _check_state_content(self, state):
        @failable
        def wrapper():
            for target_table_name, target_table_info in self.target_states[state]["tables"].items():
                target_table_tuples = target_table_info["values"]
                actual_table_tuples = self.database.get_table_data(target_table_name)
                if sorted(target_table_tuples) != sorted(actual_table_tuples):
                    return False

            return True

        return wrapper

    def _check_state_keys(self, state):
        @failable
        def wrapper():
            for target_table_name, target_table_keys in self.target_states[state]["keys"].items():
                # Primary key
                target_table_primary_key = target_table_keys["primary"]["column_name"]
                actual_table_primary_key = self.database.get_table_primary_key(target_table_name)
                if not actual_table_primary_key or target_table_primary_key != actual_table_primary_key[0]:
                    return False

                # Foreign keys
                if "foreign" not in target_table_keys:
                    continue
                target_table_foreign_keys = target_table_keys["foreign"]
                actual_table_foreign_keys = self.database.get_table_foreign_keys(target_table_name)
                if [i for i in target_table_foreign_keys if i not in actual_table_foreign_keys]:
                    return False

            return True

        return wrapper

    def generate_report(self):
        total_student_marks = 0
        total_test_marks = 0

        for state, tests in self.grading_template.items():
            print("=================================================")
            print(f"Tests de l'état {state}:")
            print("=================================================")
            for test_name, test_status in tests.items():
                test_marks = test_status["points"]
                student_marks = test_marks if test_status["passed"] else 0

                total_student_marks += student_marks
                total_test_marks += test_marks

                print(f"    Nom du test:{test_name}")
                print(f"    Points: {student_marks} / {test_marks}")
                print("    ---")
        print(f"Total de points: {total_student_marks} / {total_test_marks}")

        if total_student_marks < total_test_marks:
            sys.exit(-1)

        sys.exit(0)


if __name__ == '__main__':
    grader = Grader()

    grader.run()

    grader.generate_report()
