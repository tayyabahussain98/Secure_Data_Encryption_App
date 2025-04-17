# 🔐 Secure_Data_Encryption_App

A simple and beginner-friendly Streamlit app to **securely store and retrieve encrypted data** using a passkey. Built with 💖 by **Tayyaba**.

---

## ✨ Features

- Store sensitive text data securely.
- Encrypt data using a passkey of your choice.
- Retrieve and decrypt the data using the correct passkey.
- Tracks failed attempts (max 3 allowed).
- Automatically locks the app after 3 failed attempts.
- Unlock access using a **Master Password** (`Admin@123`).
- Data saved locally in a `stored_data.json` file.

---

## ⚙️ Requirements

```python
Install the required Python libraries:

```bash
uv init .
uv add streamlit cryptography
```
## 🚀 How to Run
Run the app using the command:

```python
streamlit run app.py
```

## 🔐 Master Password Info
If you enter the wrong passkey 3 times, the app will lock automatically.

To unlock, go to Login Page and enter:

```python
Admin@123
```

## 💾 Data Storage
Encrypted data is saved in a file named:

```python
stored_data.json
```
Each stored record looks like this:

```python
{
  "data_id": {
    "encrypted": "<encrypted_text>",
    "passkey": "<hashed_passkey>"
  }
}
```

## 📁 Project Structure

```python
app.py              # Main Streamlit application
stored_data.json    # File where encrypted data is stored
README.md           # Project info file
```

## 🙋 Author

Made with 💖 by Tayyaba
Thank you for checking out the project!