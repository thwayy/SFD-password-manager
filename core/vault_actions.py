# CRUD operations on password vault table

import uuid

# add a new entry to the vault
def add_entry(vault, username, password, website):
        new_entry = {
                "id":str(uuid.uuid4()), #unique id so the entry can be edited or deleted
                "username":username,
                "password":password,
                "website":website
        }
        vault["entries"].append(new_entry)