import sqlite3 as s3
from typing import Union


class DataBase:
    def __init__(self):
        self.db_file_name = "profiles.db"
        self.profiles = []

    def db_operation(self, command: str, fetch=None) -> Union[list, None]:
        con = s3.connect(self.db_file_name)
        cur = con.cursor()
        if not fetch:
            result = cur.execute(command)
        else:
            result = cur.execute(command).fetchall()
        con.commit()
        con.close()
        return result

    def start(self) -> None:
        self.db_operation("CREATE TABLE IF NOT EXISTS profiles "
                          "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "ProfileName TEXT, UserName TEXT, Password TEXT)")
        self.db_operation("CREATE TABLE IF NOT EXISTS master "
                          "(Password TEXT)")

    def add_master(self, password: str) -> None:
        self.db_operation(f"INSERT INTO master "
                          f"(Password) "
                          f"VALUES ('{password}')")

    def change_master(self, new_password: str) -> None:
        self.db_operation(f"UPDATE master "
                          f"SET Password = '{new_password}';")

    def is_master(self) -> bool:
        return bool(self.db_operation("SELECT COUNT(*) AS count FROM master", fetch=True)[0][0])

    def get_master(self) -> Union[tuple, None]:
        if self.is_master():
            return self.db_operation("SELECT * FROM master", fetch=True)[0][0]
        else:
            return None

    def add_profile(self, *values: str) -> None:
        self.db_operation(f"INSERT INTO profiles "
                          f"(ProfileName, UserName, Password) "
                          f"VALUES ('{values[0]}', '{values[1]}', '{values[2]}')")

    def change_profile(self, *values: str) -> None:
        self.db_operation(f"UPDATE profiles "
                          f"SET UserName = '{values[1]}', "
                          f"Password = '{values[2]}' "
                          f"WHERE ProfileName = '{values[0]}';")

    def remove_profile(self, profile_name: str) -> None:
        self.db_operation(f"DELETE FROM profiles WHERE ProfileName = '{profile_name}'")

    def get_profiles(self) -> list:
        self.profiles = self.db_operation("SELECT * FROM profiles", fetch=True)
        return self.profiles

    def __len__(self) -> int:
        return self.db_operation("SELECT COUNT(*) AS count FROM profiles", fetch=True)[0][0]
