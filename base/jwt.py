from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import serialization

import os

import json
from datetime import datetime, timedelta, timezone

from jwt import (
    JWT,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime


def init_rsa_keys():
    if(not os.path.exists('secrets/private_key.pem') or not os.path.exists('secrets/public_key.pub')):

        os.mkdir('secrets') if not os.path.exists('secrets') else None

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key_pass = os.getenv("RSA_PASSWORD").encode()

        encrypted_pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(private_key_pass)
        )

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        private_key_file = open("secrets/private_key.pem", "w")
        private_key_file.write(encrypted_pem_private_key.decode())
        private_key_file.close()

        public_key_file = open("secrets/public_key.pub", "w")
        public_key_file.write(pem_public_key.decode())
        public_key_file.close()

def load_private_rsa_key():
    private_key_pass = os.getenv("RSA_PASSWORD").encode()

    with open("secrets/private_key.pem", "rb") as private_key_file:
        private_key = serialization.load_pem_private_key(
            private_key_file.read(),
            password=private_key_pass
        )
        private_key_bites = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

    return private_key_bites

def load_public_rsa_key():
    with open("secrets/public_key.pub", "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(
            public_key_file.read()
        )
        public_key_bites = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    return public_key_bites

def sign_jwt(payload):
    private_key = jwk_from_pem(load_private_rsa_key())

    jwt_instance = JWT()
    token = jwt_instance.encode(payload, private_key, alg='RS256')
    return token

def verify_jwt(token):
    public_key = jwk_from_pem(load_public_rsa_key())

    jwt_instance = JWT()
    try:
        payload = jwt_instance.decode(token, public_key, algorithms=['RS256'])
        expiration_time = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
        print(f"JWT expiration time: {expiration_time}")
        if expiration_time < datetime.now(timezone.utc):
            print("JWT has expired.")
            return None
        else:
            print("JWT is valid.")
       
        return payload
    except Exception as e:
        print(f"JWT verification failed: {e}")
        return None

def make_jwt_payload(user_id, expiration_minutes=60,):
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    payload = {
        "user_id": user_id,
        "exp": get_int_from_datetime(expiration_time)
    }
    return payload