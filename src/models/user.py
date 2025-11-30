import sqlite3
from typing import Any

from database.db import DatabaseConnection


class User:
    def __init__(self, row_object):
        self.id = row_object['id']
        self.role = row_object['role']
        self.firstname = row_object['firstname']
        self.lastname = row_object['lastname']
        self.dob = row_object['dob']
        self.phonenum = row_object['phonenum']
        self.email = row_object['email']
        self.address = row_object['address']
        self.password = row_object['password']

    def update(self, new_attr: dict[str, Any]):
        """
        Update user record in database and the user instance.
        Accepts a dictionary of str attributes and their new values.
        """
        if new_attr is None:
            return

        # Return concatenated str of placeholders. (ie, firstname = ?, dob = ?)
        fields = ', '.join(f"{field} = ?" for field in new_attr.keys())
        attributes = tuple(new_attr.values())
        params = attributes + (self.id,)
        try:
            # Update the user record in database.
            with DatabaseConnection() as cursor:
                cursor.execute(f"""
                UPDATE user
                SET {fields}
                WHERE id = ?
                """, params)
        except sqlite3.Error as e:
            print(f"( WARNING ⚠ ) ERROR: {e}")
            raise
        else:
            # Update the user instance.
            for attribute, value in new_attr.items():
                setattr(self, attribute, value)
