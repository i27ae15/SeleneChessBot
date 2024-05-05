from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game"
    hash = None

    def ready(self) -> None:
        import game.signals
        from pieces.utilites import ZobristHash
        if GameConfig.hash is None:
            GameConfig.hash = ZobristHash()

        return super().ready()

