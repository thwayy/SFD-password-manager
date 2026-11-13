# SFD-password-manager

Group project for Security Fundamentals and Development module CA1.

## Installation instructions
### Clone the project
```
git clone https://github.com/thwayy/SFD-password-manager.git
cd SFD-password-manager
```
### Install the packages
```
pip install -r requirements.txt
```
### Run the app
```
streamlit run app.py
```
The app opens in your browser at http://localhost:8501.
To stop it, press `Ctrl+C` in the terminal.
## User guide
1. Click **Don't have an account?** and enter a master password
   (minimum 8 characters). Remember this password.
2. Once inside the vault, use **+ Add** to save a password for a website or
   **Generate a password** to be suggested a strong, cryptographically secure password.
3. Click **Lock vault** to log out. You can log in again using the master password.
