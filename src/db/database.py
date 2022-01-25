from sqlalchemy import create_engine, update, func
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


from .config import URI
from .models import Player, Game, Base

class DB():
    def __init__(self):
        self.engine = create_engine(URI)
        self.session = sessionmaker(bind=self.engine)

    @contextmanager
    def _session_scope(self):
        # Manages session and rolls back changes if error
        s = self.session()
        try:
            yield s
            s.commit()
        except Exception:
            s.rollback()
            raise
        finally:
            s.close()

    def start(self) -> None:
        # Preps database
        # Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def player_exists(self, name: str) -> bool:
        # Returns true if player exists in Player table, false otherwise
        with self._session_scope() as s:
            player = s.query(Player).filter_by(name=name).first()
            return player != None

    def add_player(self, name: str) -> None:
        # Adds a new player row to the database
        player = Player(name=name, high_score=0)
        with self._session_scope() as s:
            s.add(player)

    def get_players(self) -> list:
        """
        Returns list of two-element tuples.
        """
        with self._session_scope() as s:
            players = s.query(Player).all()
            return [(player.name, player.high_score) for player in players]

    def get_games(self) -> list:
        """
        Returns list of two-element tuples.
        """
        with self._session_scope() as s:
            games = s.query(Game, Player).join(Player).all()
            print(games[0])
            return [(player.name, game.score, game.date.strftime("%d/%m/%y")) for game, player in games]

    def add_game(self, name: str, score: int) -> None:
        is_high_score = False
        # Adds a new game to the database
        with self._session_scope() as s:
            player = s.query(Player).filter_by(name=name).first()
            game = Game(
                player_id=player.id,
                score=score,
                date= func.now()
            )
            s.add(game)
            # Update the high score
            if score > player.high_score:
                is_high_score = player.high_score != 0
                s.execute(
                    update(Player).
                    where(Player.name == player.name).
                    values(high_score=score)
                )
            return is_high_score
