"""Crea usuarios deterministas para la suite Cypress.

Reutiliza el seed de desarrollo local.

Ejecutar desde backend/:

    python -m scripts.seed_e2e
"""

from scripts.seed_users import DEV_PASSWORD, seed


if __name__ == "__main__":
    emails = seed()
    print("Usuarios E2E listos: admin, teacher, student /", DEV_PASSWORD)
    for email in emails:
        print(f"  - {email}")
