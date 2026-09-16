from app.core.database import engine

try:
    with engine.connect() as connection:
        print("✅ Connexion à PostgreSQL réussie !")
except Exception as e:
    print("❌ Erreur de connexion :", e)