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


# change existing entry 
def edit_entry(vault, entry_id, username, password, website):
        for entry in vault["entries"]:
                if entry["id"]==entry_id:
                        entry["username"]=username
                        entry["password"]=password
                        entry["website"]=website


# remove an entry
def delete_entry(vault, entry_id):
        for entry in vault["entries"]:
                if entry["id"]==entry_id:
                        vault["entries"].remove(entry)
                        return

