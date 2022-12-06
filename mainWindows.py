import MineSweeperWindows
import TimerWindows

app = TimerWindows.Timer()
app.title('Timer')
game = MineSweeperWindows.MineSweeper()
MineSweeperWindows.MineSweeper.start_game(game)
