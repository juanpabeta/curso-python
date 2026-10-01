from passlib.context import CryptContext

HASH_SCHEME = "argon2"

pwd_context = CryptContext(schemes = [HASH_SCHEME],deprecated = "auto")

def hash_password(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password: str):
    if not pwd_context.verify(plain_password,hashed_password):
        raise ValueError("contraseña incorrecta")
    

def main():
    print("*** Registro de Usuario ***")
    password_registrado = input("Por favor, introduce una contraseña para ingresar: ")
    hashed = hash_password(password_registrado)
    print(f"hash generado: {hashed}")
    
    
    print("\n ---Prueba de contraseña ---")
    
    try:
        verify_password(password_registrado,hashed)
        print("Contraseña correcta: Login exitoso")
    except ValueError as e:
        print(f"Error: {e}")
        
if __name__ == "__main__":
    main()