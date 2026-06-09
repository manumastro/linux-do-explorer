#!/usr/bin/env python3
"""
Script per crittografare le password e API key in VPS-STACK-RELAY.md
Utilizza XOR con la chiave fornita per crittografare i dati sensibili.
"""

import re
import base64
import hashlib

def xor_encrypt(data: str, key: str) -> str:
    """Crittografa i dati usando XOR con la chiave."""
    key_hash = hashlib.sha256(key.encode()).digest()
    encrypted = []
    for i, char in enumerate(data):
        encrypted.append(chr(ord(char) ^ key_hash[i % len(key_hash)]))
    return base64.b64encode(''.join(encrypted).encode('latin-1')).decode()

def xor_decrypt(encrypted_data: str, key: str) -> str:
    """Decrittografa i dati usando XOR con la chiave."""
    key_hash = hashlib.sha256(key.encode()).digest()
    decoded = base64.b64decode(encrypted_data).decode('latin-1')
    decrypted = []
    for i, char in enumerate(decoded):
        decrypted.append(chr(ord(char) ^ key_hash[i % len(key_hash)]))
    return ''.join(decrypted)

# Pattern per identificare dati sensibili
SENSITIVE_PATTERNS = [
    # API keys (sk-*, fe_*, etc.)
    r'sk-[A-Za-z0-9_-]{20,}',
    r'fe_oa_[A-Za-z0-9]{20,}',
    r'sk-cp-[A-Za-z0-9_-]{20,}',
    r'sk-or-v1-[A-Za-z0-9]{20,}',
    r'grok-local-[A-Za-z0-9]{20,}',
    r'nvapi-[A-Za-z0-9_-]{20,}',
    r'modalresearch_[A-Za-z0-9]{20,}',
    r'db41d9a8c35746d49801900c289bffbe\.[A-Za-z0-9]{20,}',
    # Passwords
    r'Password\s*\|\s*`([^`]+)`',
    # JWT tokens
    r'eyJ[A-Za-z0-9_-]{50,}',
    # OAuth refresh/access tokens
    r'ghu_[A-Za-z0-9]{20,}',
    r'1//0[A-Za-z0-9_-]{20,}',
    r'ya29\.[A-Za-z0-9_-]{20,}',
    r'r9Wz-[A-Za-z0-9_-]{20,}',
    r'0IzAv[A-Za-z0-9_-]{20,}',
    r'XRHMNLjuhgUjSktX4q7lrgWNK',
    r'rt__[A-Za-z0-9_.-]{20,}',
]

def encrypt_file(input_file: str, output_file: str, key: str):
    """Crittografa tutti i dati sensibili nel file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trova e crittografa tutti i pattern sensibili
    encrypted_content = content
    found_items = []
    
    # Crittografa le password nella tabella 13.1
    password_pattern = r'(\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|)\s*`([^`]+)`\s*\|'
    def replace_password(match):
        prefix = match.group(1)
        password = match.group(2)
        if password not in ['(OAuth GitHub)', '(login email; API key sotto)', '(console RK API)', '(prob. OpenAI-compatible)']:
            encrypted = xor_encrypt(password, key)
            found_items.append(f"Password: {password[:10]}...")
            return f'{prefix} `ENC:{encrypted[:20]}...` |'
        return match.group(0)
    
    encrypted_content = re.sub(password_pattern, replace_password, encrypted_content)
    
    # Crittografa API keys
    for pattern in SENSITIVE_PATTERNS:
        matches = re.findall(pattern, encrypted_content)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0]
            if len(match) > 15:  # Solo crittografa chiavi lunghe
                encrypted = xor_encrypt(match, key)
                found_items.append(f"Key: {match[:15]}...")
                encrypted_content = encrypted_content.replace(match, f'ENC:{encrypted[:30]}...')
    
    # Crittografa i JWT token completi
    jwt_pattern = r'eyJ[A-Za-z0-9_-]{50,}'
    for match in re.findall(jwt_pattern, encrypted_content):
        encrypted = xor_encrypt(match, key)
        found_items.append(f"JWT: {match[:20]}...")
        encrypted_content = encrypted_content.replace(match, f'ENC:{encrypted[:30]}...')
    
    # Scrivi il file crittografato
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted_content)
    
    print(f"✅ File crittografato: {output_file}")
    print(f"📊 Elementi crittografati: {len(found_items)}")
    for item in found_items[:10]:  # Mostra solo i primi 10
        print(f"   - {item}")
    if len(found_items) > 10:
        print(f"   ... e altri {len(found_items) - 10} elementi")

def decrypt_file(input_file: str, output_file: str, key: str):
    """Decrittografa tutti i dati sensibili nel file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trova e decrittografa tutti i pattern ENC:
    decrypted_content = content
    enc_pattern = r'ENC:([A-Za-z0-9+/=]+?)(?:\.\.\.)?'
    
    def replace_encrypted(match):
        encrypted = match.group(1)
        try:
            decrypted = xor_decrypt(encrypted, key)
            return decrypted
        except:
            return match.group(0)
    
    decrypted_content = re.sub(enc_pattern, replace_encrypted, decrypted_content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_content)
    
    print(f"✅ File decrittografato: {output_file}")

if __name__ == "__main__":
    import sys
    
    key = "Manu200212??!!??!!??"
    input_file = "VPS-STACK-RELAY.md"
    encrypted_file = "VPS-STACK-RELAY-ENCRYPTED.md"
    
    if len(sys.argv) > 1 and sys.argv[1] == "decrypt":
        if len(sys.argv) > 2:
            encrypted_file = sys.argv[2]
        decrypt_file(encrypted_file, input_file, key)
    else:
        encrypt_file(input_file, encrypted_file, key)
        print(f"\n📝 Per decrittografare: python3 encrypt_vps.py decrypt {encrypted_file}")
