import tkinter
import random

ROWS = 25
COLS =25
TILE_SIZE =25

WINDOW_WIDTH=TILE_SIZE*ROWS
WINDOW_HEIGHT=TILE_SIZE*COLS

class tile:
    def __init__(self, x, y):
            self.x=x
            self.y=y
    

#game window
window=tkinter.Tk()
window.title("snake")
window.resizable(False,False)

canvas = tkinter.Canvas(window,bg="black",width=WINDOW_WIDTH,height= WINDOW_HEIGHT,borderwidth=0,highlightthickness=0)
canvas.pack()
window.update()

#center the window
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

window_x= int((screen_width/2) - (window_width/2))
window_y= int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
#initialize game
snake =tile(5*TILE_SIZE,5*TILE_SIZE)#single tile,snakes head
food=(tile(10*TILE_SIZE,10*TILE_SIZE))
velocityx=0
velocityy=0
def change_direction(e):#e means event
      print(e)

def draw():
      global snake
      #draw snake
      canvas.create_rectangle(snake.x,snake.y,snake.x+TILE_SIZE,snake.y+TILE_SIZE,fill="purple")
      #draw snake
      canvas.create_rectangle(food.x,food.y,food.x+TILE_SIZE,food.y+TILE_SIZE,fill="lime green")


      window.after(100,draw)#10fps/sec
draw()
window.bind("<keyrelease>", change_direction)
window.mainloop()

