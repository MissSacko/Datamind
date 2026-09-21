from app.core.database import SessionLocal
from app.models.user import User
from app.models.dataset import Dataset
from app.models.conversation import Conversation
from app.models.message import Message


def test_conversation_message_relationships_and_cascade():
    db = SessionLocal()

    try:
        # 1. Créer un utilisateur
        user = User(
            name="Test",
            first_name="Kadi",
            email="conversation@test.com",
            password_hash="fake_hash",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 2. Créer un dataset
        dataset = Dataset(
            user_id=user.id,
            name="Ventes 2025",
            source_type="file",
            file_name="ventes.csv",
            file_size=2048,
            storage_key="test/ventes.csv",
        )
        db.add(dataset)
        db.commit()
        db.refresh(dataset)

        # 3. Créer une conversation liée au dataset
        conversation = Conversation(
            user_id=user.id,
            dataset_id=dataset.id,
            title="Analyse des ventes 2025",
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        # 4. Ajouter plusieurs messages
        message_1 = Message(
            conversation_id=conversation.id,
            role="user",
            content="Montre-moi les ventes de 2025.",
        )

        message_2 = Message(
            conversation_id=conversation.id,
            role="assistant",
            content="Voici l'analyse des ventes de 2025.",
            message_metadata={
                "analysis_id": 1,
                "tools_used": ["filter_data", "aggregate_data"],
            },
        )

        message_3 = Message(
            conversation_id=conversation.id,
            role="tool",
            content="Résultat du filtrage : 125 lignes.",
            message_metadata={
                "tool": "filter_data",
            },
        )

        db.add_all([message_1, message_2, message_3])
        db.commit()

        # Garder les IDs avant les suppressions
        conversation_id = conversation.id
        message_1_id = message_1.id
        message_2_id = message_2.id
        message_3_id = message_3.id
        dataset_id = dataset.id

        # 5. Vérifier la relation Conversation → Messages
        db.refresh(conversation)

        assert len(conversation.messages) == 3
        assert conversation.messages[0].conversation_id == conversation.id

        # 6. Vérifier le JSONB message_metadata
        assert message_2.message_metadata["analysis_id"] == 1
        assert "filter_data" in message_2.message_metadata["tools_used"]

        # 7. Supprimer le dataset
        db.delete(dataset)
        db.commit()

        # Le dataset doit disparaître
        assert db.get(Dataset, dataset_id) is None

        # Mais la conversation doit rester
        remaining_conversation = db.get(
            Conversation,
            conversation_id,
        )

        assert remaining_conversation is not None

        # Et dataset_id doit devenir NULL
        assert remaining_conversation.dataset_id is None

        # 8. Supprimer la conversation
        db.delete(remaining_conversation)
        db.commit()

        # La conversation doit disparaître
        assert db.get(Conversation, conversation_id) is None

        # Et les messages doivent être supprimés par CASCADE
        assert db.get(Message, message_1_id) is None
        assert db.get(Message, message_2_id) is None
        assert db.get(Message, message_3_id) is None

        # 9. Nettoyer l'utilisateur
        db.delete(user)
        db.commit()

    finally:
        db.close()