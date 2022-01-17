from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update 
from contextlib import contextmanager
from models import Player, Game, Base
from config import URI

engine = create_engine(URI)
Session = sessionmaker(bind=engine)

@contextmanager
def _session_scope():
    # Manages session and rolls back changes if error
    s = Session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()

def start() -> None:
    # Preps database
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def new_player(name: str):
    # Adds a new player row to the database
    player = Player(name=name, high_score=0)
    with _session_scope() as s:
        s.add(player)


def add_game(name: str, score: int) -> None:
    # Adds a new game to the database
    player = Player.query.filter_by(name=name)
    game = Game(
        player_id=player.id,
        score=score
    )

    with _session_scope() as s:
        s.add(game)
        # Update the high score
        if score > player.high_score:
            s.execute(
                update(Player).
                where(Player.name == player.name).
                values(high_score=score)
            )
