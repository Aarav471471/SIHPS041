import os
from ecdsa import SigningKey, VerifyingKey, NIST256p
import base64
import json

KEY_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "keys")
PUB_KEY_PATH = os.path.join(KEY_PATH, "cert_pub.pem")

def get_private_key():
    pem = os.getenv("ES256_PRIVATE_KEY_PEM")
    if pem:
        return SigningKey.from_pem(pem)
    
    # Fallback for dev: read from file
    priv_path = os.path.join(KEY_PATH, "cert_priv.pem")
    if os.path.exists(priv_path):
        with open(priv_path, "rb") as f:
            return SigningKey.from_pem(f.read())
    return None

def ensure_keys():
    os.makedirs(KEY_PATH, exist_ok=True)
    priv_path = os.path.join(KEY_PATH, "cert_priv.pem")
    
    if not os.getenv("ES256_PRIVATE_KEY_PEM") and not os.path.exists(priv_path):
        print("Generating new ES256 key pair for dev...")
        sk = SigningKey.generate(curve=NIST256p)
        vk = sk.verifying_key
        with open(priv_path, "wb") as f:
            f.write(sk.to_pem())
        with open(PUB_KEY_PATH, "wb") as f:
            f.write(vk.to_pem())

def sign_payload(payload_dict: dict) -> str:
    sk = get_private_key()
    if not sk:
        raise Exception("No private key available for signing")
    
    payload_json = json.dumps(payload_dict, separators=(',', ':'), sort_keys=True)
    signature = sk.sign(payload_json.encode('utf-8'))
    return base64.urlsafe_b64encode(signature).decode('utf-8')

def verify_signature(payload_json: str, signature_b64: str) -> bool:
    if not os.path.exists(PUB_KEY_PATH):
        return False
    with open(PUB_KEY_PATH, "rb") as f:
        vk = VerifyingKey.from_pem(f.read())
    
    signature = base64.urlsafe_b64decode(signature_b64)
    try:
        return vk.verify(signature, payload_json.encode('utf-8'))
    except:
        return False
