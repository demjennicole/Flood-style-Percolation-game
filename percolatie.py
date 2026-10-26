#Percolation game ("flood-it" style game)
# The board is an n x n grid of colored squares. The "region" is the group of
# connected squares, starting from the corner (0,0), that all share the same
# color. Each click on the palette recolors the whole region with the chosen
# color, and the region absorbs any neighbouring squares that already have
# that color. The goal: make the whole board one color in as few clicks as
# possible.

import turtle
import random

t=turtle.Turtle()
s=turtle.Screen()


def draw_square(turtle, color, a, x, y):
  """Draw one filled square of side `a` with its bottom-left corner at (x, y).
The parameter `turtle` shadows the module name inside this function; it is
the Turtle object passed in, e.g. `t`. """
  turtle.penup()
  turtle.color(color)
  turtle.fillcolor(color)
  turtle.goto(x,y)
  turtle.pendown()
  turtle.begin_fill()
  for i in range (4):
    turtle.forward(a)
    turtle.left(90)
  turtle.end_fill()
  turtle.setheading(0)

# ---------------------------------------------------------------------------
# Global settings, unpacked from one tuple on a single line:
#   a      = side length of one square (pixels)
#   bx, by = bottom-left corner of the game board
#   c      = leftover value (150); not used anywhere else, see note in fun2
#   n      = the board is n x n squares
#   color  = leftover value (0); not used anywhere else

a,bx,by,c,n,color=(33,-200,-300,150,11,0)

# Bottom-left corner of the color palette (the row of clickable squares)
cx,cy=-200,100

# Q is the list of squares that currently belong to the region
# connected to the corner (0, 0). It starts with just that corner.
Q=[[0,0]]

# L is the board: L[i][j] holds the color INDEX (into Lcol) of the square in
# column i, row j. Starts as an n x n grid of zeros; filled randomly later.
L=[[0]*n for i in range(n)]

#Colors for the quares
Lcol=['pink','plum','salmon','deeppink','lightpink3']

# LL = [0, 1, 2, 3, 4]: the color indices in palette order.
# The palette square at position i shows color Lcol[LL[i]].
LL=[i for i in range(len(Lcol))]

nr_click=0 #number of clicks made so far
win=False  #becomes true when the player finishes the game

#title and instructions
t.penup()
t.goto(-220,300)
t.write("Percolation game",font=("Broadway", 30, "normal"))
t.penup()
t.goto(-420,200)
t.write("Click whichever color you want, your goal is to get a monocrome square with the minimum number of clicks", font=("Arial", 16, "normal"))

def palette(LL,bx,by):
    """Draws the palette: one square per color, side by side in a row,
     starting at (bx, by)."""
    turtle.tracer(0) #turns animation off, so you can see everything at once in the end
    for i in range(len(LL)):
        draw_square(t,Lcol[LL[i]],a,a*i+bx,by)
    turtle.tracer(1) #puts the animation back on

def drawing(L,bx,by):
    """Fills the board with random colors and draws it.
     Called once at the start. L[i][j] is set to a random color index, and the
    square is drawn at x = a*i + bx, y = a*j + by (i = column, j = row)."""
    turtle.tracer(0)
    for i in range(len(L[0])):
        for j in range(len(L[0])):
            L[i][j]=int(random.random()*len(Lcol))
            draw_square(t,Lcol[L[i][j]],a,a*i+bx,a*j+by)
    turtle.tracer(1)

def recolor(L,bx,by):
    """Redraws the board from the current contents of L, without changing it.
    It is used after every click to show the recolored region."""
    turtle.tracer(0)
    for i in range(len(L[0])):
        for j in range(len(L[0])):
            draw_square(t, Lcol[L[i][j]], a, a * i + bx, a * j + by)
    turtle.tracer(1)

def neighbours(q):
    """Returns the list of squares adjacent to q (up, left, down, right),
    keeping only those that lie inside the n x n board."""
    r,c=q
    V=[]
    if r>0:
        V.append([r-1,c])
    if c>0:
        V.append([c-1,r])
    if r<n-1:
        V.append([r+1,c])
    if c<n-1:
        V.append([c+1,r])
    return V

def build_Q():
    """Computes the starting region: every square connected to (0, 0)
    through squares of the same color as the corner."""
    global Q
    Q = [(0, 0)] #restarts the region from the corner
    color= L[0][0] #the region's color
    c = True #"Did the region really grow?"
    while c:
        c = False
        #it iterates over a copy of Q, as we append to Q inside the loop
        for q in list(Q):
            for V in neighbours(q):
                if V not in Q:
                    i, j = V
                    if L[i][j] == color: # if they have the same color then it joins the region
                        Q.append(V)
                        c = True
    #the loop fully ends when a full pass adds nothing new, so there is no infinite loop

def flood(color1):
    """Recolors the region with color index `color1`, then extends the region
     with any neighbouring squares that already have that color.
    Returns False if the click changed nothing (same color), True otherwise."""
    global Q
    color2=L[0][0]
    if color1==color2:
        return False
    for (i,j) in Q:
        L[i][j]=color1
    k=True
    while k:
        k=False
        for q in Q:
            for V in neighbours(q):
                if V not in Q:
                    i,j=V
                    if L[i][j]==color1:
                       Q.append(V)
                       k=True
    return True

def fun3(x,y):
    """Click handler (registered with s.onclick). If the click lands on a
    palette square and the game isn't over, play that color."""
    global nr_click
    i,j=(x-cx)/a,(y-cy)/a
    if 0<=i<len(Lcol) and 0<=j<1 and not win:
        chosen=int(i)
        changed=flood(chosen)
        if changed:
            nr_click+=1
        recolor(L,bx,by)
        palette(LL,cx,cy)
        winner()

def winner():
    """Checks if the game has been won or not."""
    global win
    if len(Q)==(n*n)+1:
        win=True
        t.penup()
        t.goto(200, -150)
        t.write("Congratulations!", font=("Arial", 16, "normal"))
        t.penup()
        t.goto(200,-170)
        t.write("You won with ", font=("Arial", 16, "normal"))
        t.penup()
        t.goto(330,-170)
        t.write(str(nr_click), font=("Arial", 16, "normal"))
        t.penup()
        t.goto(355,-170)
        t.write("clicks", font=("Arial", 16, "normal"))

# ---------------------------------------------------------------------------
# Program start
palette(LL,cx,cy) #draws the palette
drawing(L,bx,by)  #creates and draws the random board
build_Q()         #finds the starting region around the corner
recolor(L,bx,by)  #redraws the board
s.onclick(fun3)   #every click on the window call fun3(x,y)
turtle.done()     #keeps the window open and waits for events
