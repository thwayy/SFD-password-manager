import json
import os
VAULT_FILE="vault.json"
def load_vault():
    if not os.path.exists(VAULT_FILE):
        return {"entries": []}
    with open(VAULT_FILE, "r") as file:
        return json.load(file)

def save_vault(vault):
    with open(VAULT_FILE, "w") as file:
            json.dump(vault, file, indent=2)