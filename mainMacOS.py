import MineSweeperMacOS
import TimerMacOS


app = TimerMacOS.Timer()
app.title('Timer')
game = MineSweeperMacOS.MineSweeper()
MineSweeperMacOS.MineSweeper.start_game(game)
