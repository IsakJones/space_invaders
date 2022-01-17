from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    high_score = Column(Integer)
    games = relationship("Game", backref="games", passive_deletes=True)

    def __repr__(self):
        return f"<Player (name = '{self.name}', high score = {self.high_score})>"

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    player_id = Column(Integer, ForeignKey(column="players.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"<Game (player_id = '{self.player_id}', score = {self.score}"

