from django.db import models


class GameState(models.Model):

    """
    This also should act as the node in the AlphaZero tree.
    """

    __tablename__ = 'game_state'

    # Relationship to self
    parent = relationship(
        'GameState',
        remote_side=[id],
        back_populates='children'
    )
    children = relationship(
        'GameState',
        back_populates='parent'
    )

    id: str = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    player_turn: str = Column(Integer, nullable=False)
    is_game_terminated: str = Column(Boolean, nullable=False)

    white_value: float = Column(Float, nullable=False)
    black_value: float = Column(Float, nullable=False)

    castleling_rights: dict = Column(JSON, nullable=False)
    fen: str = Column(String, nullable=False)
