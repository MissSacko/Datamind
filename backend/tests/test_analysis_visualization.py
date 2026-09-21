from app.core.database import SessionLocal
from app.models.user import User
from app.models.dataset import Dataset
from app.models.analysis import Analysis
from app.models.visualization import Visualization


def test_analysis_visualization_cascade():
    db = SessionLocal()

    try:
        # 1. Créer un utilisateur
        user = User(
            name="Test",
            first_name="Kadi",
            email="analysis@test.com",
            password_hash="fake_hash",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 2. Créer un dataset
        dataset = Dataset(
            user_id=user.id,
            name="Dataset test",
            source_type="file",
            file_name="test.csv",
            file_size=1024,
            storage_key="test/test.csv",
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        # 3. Créer une analyse
        analysis = Analysis(
            user_id=user.id,
            dataset_id=dataset.id,
            analysis_type="descriptive_statistics",
            question="Quelle est la moyenne des ventes ?",
            result={
                "mean": 125000,
                "median": 118000,
                "count": 100,
            },
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        # 4. Créer deux visualisations
        visualization_1 = Visualization(
            analysis_id=analysis.id,
            chart_type="bar",
            title="Ventes par mois",
            config={
                "x": "month",
                "y": "sales",
            },
        )

        visualization_2 = Visualization(
            analysis_id=analysis.id,
            chart_type="line",
            title="Évolution des ventes",
            config={
                "x": "date",
                "y": "sales",
            },
        )

        db.add_all([visualization_1, visualization_2])
        db.commit()

        # Garder les IDs avant suppression
        analysis_id = analysis.id
        visualization_1_id = visualization_1.id
        visualization_2_id = visualization_2.id

        # 5. Vérifier la relation
        db.refresh(analysis)

        assert len(analysis.visualizations) == 2
        assert analysis.result["mean"] == 125000
        assert visualization_1.config["x"] == "month"

        # 6. Supprimer l'analyse
        db.delete(analysis)
        db.commit()

        # 7. Vérifier le CASCADE
        assert db.get(Analysis, analysis_id) is None
        assert db.get(Visualization, visualization_1_id) is None
        assert db.get(Visualization, visualization_2_id) is None
        

        # Nettoyage
        db.delete(user)
        db.commit()

    finally:
        db.close()