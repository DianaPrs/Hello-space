import time
import asyncio
import random
import curses
import subprocess
from client import Client

COROUTINES = []


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


def draw(canvas):
    """Draw stars in terminal"""

    h, w = canvas.getmaxyx()
    curses.curs_set(False)
    canvas.border()
    COROUTINES.append(morning_star(canvas))
    client = Client("127.0.0.1", 8888, timeout=15)
    #borders = client.put(h, w)
    stars = client.data

    for _ in range(stars):
        symbol = random.choice('+*.:')
        row = random.randint(1, h - 2)
        column = random.randint(1, w - 2)
        COROUTINES.append(blink(canvas, row, column)) 
        COROUTINES.append(light_up(canvas, row, column, symbol))
         
    while True:
        for coroutine in COROUTINES.copy():
          try:
            coroutine.send(None)
            canvas.refresh() 
            time.sleep(0.01)
          except StopIteration:
            COROUTINES.remove(coroutine)
          if len(COROUTINES) == 0:
              break
        canvas.refresh()

async def morning_star(canvas, start_row=0, start_column=40, rows_speed=5, columns_speed=-5):
    """Display animation of first star"""
    row, column = start_row, start_column
    row += rows_speed
    column += columns_speed

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    
    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), '/', curses.A_DIM)
        canvas.refresh()
        time.sleep(0.2)

        canvas.addstr(round(row), round(column), ' ')
        canvas.refresh()

        row += rows_speed
        column += columns_speed   

    canvas.addstr(round(row - 3), round(column + 3), '*')
    canvas.refresh()   
    time.sleep(0.1) 
    curses.beep()  
    canvas.addstr(round(row - 3), round(column + 3), '*', curses.A_BOLD)
    canvas.refresh()
    starfall(canvas)
    await asyncio.sleep(0)

async def light_up(canvas, row, column, symbol):
    """Lights the stars"""
    while True:
        canvas.addstr(row, column, symbol)
        await Sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await Sleep(5)

        canvas.addstr(row, column, symbol)
        await Sleep(3)

async def blink(canvas, row, column):
    """Change star intensity"""
    while True:
        canvas.addstr(row, column, ' ')
        canvas.refresh()
        await Sleep(200)
        
def starfall(canvas):
    """Launch starfall"""
    print(f"Hello, space!")


if __name__ == '__main__':
    subprocess.call(['/usr/bin/resize', '-s', '20', '85'])
    curses.update_lines_cols()
    curses.wrapper(draw)

