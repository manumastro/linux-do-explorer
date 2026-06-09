#!/usr/bin/env python3
"""
Script per crittografare SOLO le password e API key in VPS-STACK-RELAY.md
Versione 2 - più mirata e precisa.
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

def encrypt_file(input_file: str, output_file: str, key: str):
    """Crittografa solo i dati sensibili nel file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Definisci i pattern sensibili con i loro replacement
    replacements = [
        # Passwords nel formato `Manu200212`
        (r'`Manu200212`', '`ENC:' + xor_encrypt('Manu200212', key) + '`'),
        
        # Passwords nel formato / Manu200212 (senza backticks)
        (r'/ Manu200212', '/ ENC:' + xor_encrypt('Manu200212', key)),
        
        # API keys sk-* (lunghezza > 20)
        (r'sk-[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # fe_oa_* keys
        (r'fe_oa_[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # sk-cp-* keys (MiniMax)
        (r'sk-cp-[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # sk-or-v1-* keys (OpenRouter)
        (r'sk-or-v1-[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # grok-local-* keys
        (r'grok-local-[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # nvapi-* keys (NVIDIA)
        (r'nvapi-[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # modalresearch_* keys
        (r'modalresearch_[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Ollama cloud keys
        (r'db41d9a8c35746d49801900c289bffbe\.[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # JWT tokens (eyJ...)
        (r'eyJ[A-Za-z0-9_-]{50,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # GitHub OAuth tokens (ghu_*)
        (r'ghu_[A-Za-z0-9]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Google OAuth refresh tokens (1//0...)
        (r'1//0[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Google OAuth access tokens (ya29.*)
        (r'ya29\.[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Qwen OAuth tokens
        (r'r9Wz-[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        (r'0IzAv[A-Za-z0-9_-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Cline OAuth tokens
        (r'XRHMNLjuhgUjSktX4q7lrgWNK', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # OpenAI refresh tokens (rt__...)
        (r'rt__[A-Za-z0-9_.-]{20,}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
        
        # Account IDs (UUID-like)
        (r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', lambda m: 'ENC:' + xor_encrypt(m.group(), key)),
    ]
    
    encrypted_content = content
    encrypted_count = 0
    
    for pattern, replacement in replacements:
        if callable(replacement):
            # Conta le occorrenze prima di sostituire
            matches = re.findall(pattern, encrypted_content)
            encrypted_count += len(matches)
            encrypted_content = re.sub(pattern, replacement, encrypted_content)
        else:
            matches = re.findall(pattern, encrypted_content)
            encrypted_count += len(matches)
            encrypted_content = encrypted_content.replace(pattern, replacement)
    
    # Aggiungi note critiche
    encrypted_content = encrypted_content.replace(
        '> ⚠️ **Sicurezza:** questo file contiene **password e chiavi API in chiaro**. Non committarlo su repo pubblici. Sul VPS: `chmod 600 VPS-STACK-RELAY.md`.',
        '> 🔐 **Sicurezza:** questo file contiene **password e chiavi API crittografate**. Per decrittografare: `python3 encrypt_vps_v2.py decrypt VPS-STACK-RELAY-ENCRYPTED.md`'
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(encrypted_content)
    
    print(f"✅ File crittografato: {output_file}")
    print(f"📊 Elementi crittografati: {encrypted_count}")

def decrypt_file(input_file: str, output_file: str, key: str):
    """Decrittografa tutti i dati sensibili nel file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern per trovare i dati crittografati
    enc_pattern = r'ENC:([A-Za-z0-9+/=]+)'
    
    def replace_encrypted(match):
        encrypted = match.group(1)
        try:
            decrypted = xor_encrypt(encrypted, key)  # XOR è simmetrico
            return decrypted
        except:
            return match.group(0)
    
    decrypted_content = re.sub(enc_pattern, replace_encrypted, content)
    
    # Ripristina la nota originale
    decrypted_content = decrypted_content.replace(
        '> 🔐 **Sicurezza:** questo file contiene **password e chiavi API crittografate**. Per decrittografare: `python3 encrypt_vps_v2.py decrypt VPS-STACK-RELAY-ENCRYPTED.md`',
        '> ⚠️ **Sicurezza:** questo file contiene **password e chiavi API in chiaro**. Non committarlo su repo pubblici. Sul VPS: `chmod 600 VPS-STACK-RELAY.md`.'
    )
    
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
        print(f"\n📝 Per decrittografare: python3 encrypt_vps_v2.py decrypt {encrypted_file}")
