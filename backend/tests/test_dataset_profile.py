from app.core.database import SessionLocal
from app.models.user import User
from app.models.dataset import Dataset
from app.models.dataset_profile import DatasetProfile
from app.models.column_profile import ColumnProfile


def test_dataset_profiling_relationships():
    db = SessionLocal()

    try:
        user = User(
            name="Test",
            first_name="Profiling",
            email="profiling.test@datamind.local",
            profession="Data Analyst",
            password_hash="fake_hash_for_test",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        dataset = Dataset(
            user_id=user.id,
            name="Sales Dataset",
            source_type="file",
            file_name="sales.csv",
            file_size=2048,
            storage_key=f"users/{user.id}/datasets/sales.csv",
        )

        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        profile = DatasetProfile(
            dataset_id=dataset.id,
            row_count=1000,
            column_count=5,
            missing_value_count=25,
            duplicate_row_count=10,
            quality_score=94.5,
            details={
                "profiling_version": "1.0",
                "analysis_engine": "pandas",
            },
        )

        db.add(profile)
        db.commit()
        db.refresh(profile)

        column = ColumnProfile(
            dataset_profile_id=profile.id,
            column_name="revenue",
            data_type="float64",
            total_count=1000,
            missing_count=5,
            missing_percentage=0.5,
            distinct_count=850,
            distinct_percentage=85.0,
            is_identifier_candidate=False,
            statistics={
                "mean": 15250.75,
                "median": 12000.0,
                "min": 100.0,
                "max": 95000.0,
                "std": 8400.25,
            },
        )

        db.add(column)
        db.commit()
        db.refresh(column)

        # Dataset → Profile
        assert profile.dataset_id == dataset.id

        # Profile → ColumnProfile
        assert len(profile.columns) == 1
        assert profile.columns[0].column_name == "revenue"

        # JSONB
        assert profile.details["profiling_version"] == ""
        "1.0"
        assert column.statistics["mean"] == 15250.75

        print(f"Dataset : {dataset.name}")
        print(f"Profil : {profile.row_count} lignes")
        print(f"Quality score : {profile.quality_score}")
        print(f"Colonne : {column.column_name}")
        print(f"Mean : {column.statistics['mean']}")

        profile_id = profile.id
        column_id = column.id

        db.delete(dataset)
        db.commit()

        assert db.get(DatasetProfile, profile_id) is None
        assert db.get(ColumnProfile, column_id) is None

    finally:
        db.delete(user)
        db.commit()
        db.close()