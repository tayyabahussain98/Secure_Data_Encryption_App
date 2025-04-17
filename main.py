import streamlit as st
import hashlib
import base64
import time
import uuid
import json
from cryptography.fernet import Fernet

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def generate_key(passkey):
    key = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(key[:32])

def encrypt_data(text, passkey):
    key = generate_key(passkey)
    return Fernet(key).encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    key = generate_key(passkey)
    return Fernet(key).decrypt(encrypted_text.encode()).decode()

def reset_failed_attempts():
    st.session_state.failed_attempts = 0

def remaining_attempts():
    return max(0, 3 - st.session_state.failed_attempts)

def save_to_json():
    with open('stored_data.json', 'w') as file:
        json.dump(st.session_state.stored_data, file)

def load_from_json():
    try:
        with open('stored_data.json', 'r') as file:
            st.session_state.stored_data = json.load(file)
    
    except FileNotFoundError:
        st.session_state.stored_data = {}

load_from_json()


if 'page' not in st.session_state:
    st.session_state.page = 'Home'

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0

if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}

st.sidebar.title('Navigation')

if st.sidebar.button('🏠 Home'):
    st.session_state.page = 'Home'

if st.sidebar.button('📥 Store Data'):
    st.session_state.page = 'Store Data'

if st.sidebar.button('📥 Retrieve Data'):
    st.session_state.page = 'Retrieve Data'

if st.sidebar.button('🔑 Login Page'):
    st.session_state.page = 'Login'


if st.session_state.failed_attempts >= 3 and st.session_state.page != 'Login':
    st.session_state.page = 'Login'

if st.session_state.page == 'Home':
    st.title('🔐 Secure Data Encryption App')
    st.write('Simple system to store and retrieve encrypted data.')
    st.info(f'Stored Data Entries: {len(st.session_state.stored_data)}')

elif st.session_state.page == 'Store Data':
    st.title('📥 Store Data')
    data = st.text_area('Enter Your Data:')
    passkey = st.text_input('Enter Passkey:', type = 'password')
    confirm = st.text_input('Confirm Passkey:', type = 'password')

    if st.button('Save'):
        if data and passkey and passkey == confirm:
            data_id = str(uuid.uuid4())
            encrypted = encrypt_data(data, passkey)
            st.session_state.stored_data[data_id] = {
                'encrypted': encrypted,
                'passkey': hash_passkey(passkey)
            }

            save_to_json()
            st.success('Data Stored Succesfully!')
            st.write('## Your Data ID')
            st.code(data_id)

        else:
            st.error('Please enter valid and matching passkeys.')


elif st.session_state.page == 'Retrieve Data':
    st.title('📥 Retrieve Data')
    data_id = st.text_input('Enter Data ID:')
    passkey = st.text_input('Enter Passkey:', type = 'password')

    st.warning(f'Remaining Login Attempts: {remaining_attempts()}')

    if st.button('Retrieve'):
        if data_id in st.session_state.stored_data:
            stored = st.session_state.stored_data[data_id]

            if hash_passkey(passkey) == stored['passkey']:
                try:
                    decrypted = decrypt_data(stored['encrypted'], passkey)
                    st.success('Decrypted Successfully!')
                    st.write('## Your Decrypted Data')
                    st.code(decrypted)
                    reset_failed_attempts()

                except:
                    st.session_state.failed_attempts += 1
                    st.session_state.last_attempt_time = time.time()
                    st.error('Incorrect Passkey!')

            else:
                st.session_state.failed_attempts += 1
                st.session_state.last_attempt_time = time.time()
                st.error('Incorrect Passkey!')

        else:
            st.error('Invalid Data ID')

elif st.session_state.page == 'Login':
    st.title('🔑 Master Login')
    if time.time() - st.session_state.last_attempt_time < 10:
        st.warning('Too many failed attempts. Please wait a few seconds...')

    else:
        master = st.text_input('Enter Master Password:', type = 'password')
        if st.button('Login'):
            if master == 'Admin@123':
                reset_failed_attempts()
                st.success('Login Successful!')
                st.session_state.page = 'Home'
            
            else:
                st.session_state.failed_attempts +=1
                st.session_state.last_attempt_time = time.time()
                st.error('Incorrect Master Password')


st.markdown('---')
st.caption('🔐 Build with 💖 by Tayyaba')