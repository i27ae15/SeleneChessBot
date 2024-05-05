import uuid

from django.db import models


class GameState(models.Model):

    """
    This also should act as the node in the AlphaZero tree.
    """
    parent: 'GameState' = models.ForeignKey(
        'GameState',
        on_delete=models.CASCADE,
        related_name='children',
        null=True
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    board_hash: float = models.FloatField()

    is_game_terminated: bool = models.BooleanField()

    white_value: float = models.FloatField()
    black_value: float = models.FloatField()

    fen: str = models.CharField(max_length=255)

    num_visits: int = models.IntegerField(default=1)

    def increment_visits(self):
        self.num_visits += 1
        self.save()
