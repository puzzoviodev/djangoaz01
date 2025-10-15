import secrets
import string

def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# Gerar e exibir a SECRET_KEY
secret_key = generate_secret_key()
print(f"SECRET_KEY = '{secret_key}'")
