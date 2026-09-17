from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User
from app.models.dataset import Dataset


def test_user_dataset_relationship():
    db = SessionLocal()

    try:
        # Création de l'utilisateur
        user = User(
            name="Sacko",
            first_name="Khadijah",
            email="relation.test@datamind.local",
            profession="Data Analyst",
            password_hash="fake_hash_for_test",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Création d'un dataset appartenant à l'utilisateur
        dataset = Dataset(
            user_id=user.id,
            name="Sales Dataset",
            source_type="file",
            file_name="sales.csv",
            file_size=1024,
            storage_key=f"users/{user.id}/datasets/sales.csv",
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        # Vérifier la relation Dataset → User
        assert dataset.user.id == user.id
        assert dataset.user.email == user.email

        # Vérifier la relation User → Dataset
        db.refresh(user)

        assert len(user.datasets) == 1
        assert user.datasets[0].name == "Sales Dataset"

        print(f"User : {user.email}")
        print(f"Dataset : {dataset.name}")
        print(f"Dataset.user : {dataset.user.email}")
        print(f"Nombre de datasets : {len(user.datasets)}")

        # Vérifier la suppression du dataset
        db.delete(dataset)
        db.commit()

        statement = select(Dataset).where(Dataset.id == dataset.id)
        deleted_dataset = db.scalar(statement)

        assert deleted_dataset is None

    finally:
        # Nettoyage de l'utilisateur
        db.delete(user)
        db.commit()
        db.close()