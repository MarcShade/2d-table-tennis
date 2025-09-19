from src.game.engine import GameEngine
from src.game.state.menu_state import MenuState
from src.game.state.game_state import GameState

if __name__ == "__main__":
    engine = GameEngine()
    engine.run(GameState(engine)) # Change to MenuState once implemented