#!/usr/bin/env python3
# Copyright Kyle K. Mears, Feburary 2016

'''
To Do:
Usability
-- Make -24, 24 the max possible points
-- Fix make valid (see make valid)
-- Increase line width
-- make last fxn function like functionString graphing -- No animation, though.
--Improve collision algorithm in win function.  Use multiple
squares at different angles instead of just one.
Also, make sure the size of the squares is correct.
-- Get Spencer to make sounds.
-- power(x/5, inf) should be in tutorial
'''

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
#from matplotlib import animation
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
from numpy import *
import random
import sys
import re
import os


def collision(point, start, width, height):
    if start[0] < point[0] < start[0]+width:
        if start[1] < point[1] < start[1]+height:
            return True
    return False

def blockPositions(dot1, dot2):
    '''takes in block position and returns starting position for blocks
    that blocks top and side attacks and doesn't overlap the blocks on dots'''
    block1 = [dot1[0]- 0.5, random.randint(-25,20) - 0.5]
    block2 = [random.randint(-25,20)- 0.5, dot1[1] - 0.5]
    block3 = [dot2[0]- 0.5, random.randint(-25,20) - 0.5]
    block4 = [random.randint(-25,20)- 0.5, dot2[1] - 0.5]
    flatBlockList = [block1, block3]
    tallBlockList = [block2, block4]
    dotList = [dot1, dot2]
    collided = False
    for block in flatBlockList:
        for dot in dotList:
            if collision(dot, block, 5, 1):
                collided = True
    for block in tallBlockList:
        for dot in dotList:
            if collision(dot, block, 1, 5):
                collided = True
    if collided:
        flatBlockList, tallBlockList = blockPositions(dot1, dot2)
    return flatBlockList, tallBlockList
    
def firstGraph(dot1, dot2, flatBlockList, tallBlockList):
    '''makes first graph for users to see'''
    plt.plot(dot1[0], dot1[1], marker='o', color='c', markersize = 11)
    plt.plot(dot2[0], dot2[1], marker='o', color='orange', markersize = 11) # radius=0.7
    plt.axis((-25,25,-25,25))
    currentAxis = plt.gca()
    for block in flatBlockList:
        currentAxis.add_patch(Rectangle(block,5,1, facecolor='cornflowerblue'))
    for block in tallBlockList:
        currentAxis.add_patch(Rectangle(block,1,5, facecolor='cornflowerblue'))
    ax = plt.axes()
    ax.xaxis.set_ticks([x for x in range(-20,21,5)])
    ax.yaxis.set_ticks([y for y in range(-20,21,5)])
    plt.grid(color = 'grey', linewidth = 1.3, which = 'major')
    x = np.linspace(-25,25,1000001)
    plt.plot(x, 100**100*x, color = 'k', linestyle='dotted', linewidth = 1.6)
    plt.plot(x, 0*x, color='k', linestyle='dotted',linewidth = 1.6)
    plt.savefig('graph.png')
    plt.show()

def yieldFxn(i,x,y,line):
    ''''''
    line.set_data(y[:i*240],
                  x[:i*240]) # y,x
    return line,


def graph(lastFxnStr, dot1, dot2, turns, flatBlockList, tallBlockList):
    '''gets input and produces new graph.  Returns new fxn'''
    functionString = input()
    np.seterr(divide='ignore', invalid='ignore')
    functionString = makeValid(functionString)
    if turns % 2 == 0:
        #Player 1's turn
        firstColor = 'c'
        secondColor = 'orange'
    else:
        firstColor = 'orange'
        secondColor = 'c'
    fig = plt.figure()
    plt.plot(dot1[0], dot1[1], marker='o', color=firstColor, markersize = 11)
    plt.plot(dot2[0], dot2[1], marker='o', color=secondColor, markersize = 11) # radius=0.7
    plt.axis((-25,25,-25,25))
    ax = plt.axes()
    ax.xaxis.set_ticks([x for x in range(-20,21,5)])
    ax.yaxis.set_ticks([y for y in range(-20,21,5)])
    plt.grid(color = 'grey', linewidth = 1.3)
    x = np.linspace(-25,25,1000001)
    #plt.plot(x, eval(functionString), color = firstColor)
    plt.plot(x, eval(lastFxnStr), color = secondColor)
    plt.plot(x, 100**100*x, color = 'k', linestyle='dotted', linewidth = 1.6)
    plt.plot(x, 0*x, color='k', linestyle='dotted',linewidth = 1.6)
    yList = [y/600 for y in range(-15000,15001)]
    xList = []
    ##Type Error below: Problem converting complex to float! x^0.5 won't work! use power(x, 0.5) instead in makeValid
    for z in range(-15000,15001):
        x = z/600
        try:
            threshold = 1250
            if -threshold < (eval(functionString)) < threshold:
                xList.append(eval(functionString))
            else:
                xList.append(np.inf)
        except ZeroDivisionError:
            xList.append(np.inf)
        except:
            xList.append(np.inf) ## Not sure if right thing to append -- this deals with fractional exponents and imaginary numbers
    #print(xList)
    #print(yList)
    line, = ax.plot([], [], lw=1, color = firstColor)
    ani = animation.FuncAnimation(fig, yieldFxn, fargs = (xList, yList, line) ,interval = 0.001,
                                  frames = 126, repeat = False, blit= True)
    currentAxis = plt.gca()
    for block in flatBlockList:
        currentAxis.add_patch(Rectangle(block,5,1, facecolor='cornflowerblue'))
    for block in tallBlockList:
        currentAxis.add_patch(Rectangle(block,1,5, facecolor='cornflowerblue'))
    ax = plt.axes()
    #plt.savefig('graph.png')
    plt.show()
    return functionString

def convertX(fxnStr, newChar): ## Can this be deleted?
    '''converts x to newChar'''
    fxnList = list(fxnStr)
    for i in range(len(fxnList)):
        if fxnList[i] == 'x':
            fxnList[i] = newChar
    return "".join(fxnList)

def makeValid(fxn):
    '''takes in a function and turns it into str of evaluatable fxn code'''
    ## To do:
    ## multipliction of special characters pi, e, and inf
    if fxn == '':
        return '0*x'
    if 'x' not in fxn and 'X' not in fxn:
        fxn = 'x*0+' + fxn
    fxnList = list(fxn)
    # |stuff| -> abs(stuff) and:
    carrotList = []
    barPos = []
    for j in range(len(fxnList)):
        if fxnList[j] == 'X':
            fxnList[j] = 'x'
        elif fxnList[j] == '|':
            barPos += [j]
        elif fxnList[j] == '^':
            fxnList[j] = '**'
    if len(barPos)%2 != 0:
        return 30+0*x
    firstBar = True
    for pos in barPos:
        if firstBar:
            firstBar = False
            fxnList[pos] = 'abs('
        else:
            firstBar = True
            fxnList[pos] = ')'
    # Adds in needed multiplication signs
    for i in range(len(fxnList)):
        if fxnList[i] == '^': 
            fxnList[i] = '**' 
        if i < len(fxnList)-1:
            twoAlphanumerics1 = re.search(r'[\dx)]',fxnList[i],re.I) and re.search(r'[\w(]',fxnList[i+1],re.I)
            twoAlphanumerics2 = re.search(r'\w',fxnList[i][-1],re.I) and re.search(r'[\dx]',fxnList[i+1],re.I)
            twoDigits = re.search(r'\d',fxnList[i],re.I) and re.search(r'\d',fxnList[i+1],re.I)
            if (twoAlphanumerics1 or twoAlphanumerics2) and not twoDigits:
                fxnList[i] += '*'
    # Adds in multiplication signs for special numers pi, e, and inf
    print("".join(fxnList))
    return "".join(fxnList)

def makeDots():
    '''returns the coordinates for 2 dots as 2 lists'''
    return [random.randint(-24,24),random.randint(-24,24)],[random.randint(-24,24),
            random.randint(-24,24)]

def win(fxn, rightDot, wrongDot, flatBlockList, tallBlockList):
    '''checks if win lose or draw'''
    rightHit, wrongHit = False, False
    boxHit = False
    #Check if line intersects box
    for block in flatBlockList:
        point = block[0]
        while point < block[0] + 5:
            if block[1] <= eval(convertX(fxn, str(point))) <= block[1] + 1:
                boxHit = True
            point += 0.001
    for block in tallBlockList:
        point = block[0]
        while point < block[0] + 1:
            if block[1] <= eval(convertX(fxn, str(point))) <= block[1] + 5:
                boxHit = True
            point += 0.001
    #Square hitbox for circular dot
    point = rightDot[0]-0.6
    while point < rightDot[0]+0.6:
        if rightDot[1]-0.6 <= eval(convertX(fxn, str(point))) <= rightDot[1]+0.6:
            rightHit = True
        point += 0.001
    point = wrongDot[0]-0.6
    while point < wrongDot[0]+0.6:
        if wrongDot[1]-0.6 <= eval(convertX(fxn, str(point))) <= wrongDot[1]+0.6:
            wrongHit = True
        point += 0.001
    if boxHit:
        print("Avoid the boxes!")
        return None
    if rightHit and not wrongHit:
        print("You won!!")
        sys.exit(0)
    elif rightHit and wrongHit:
        print("Mutual Destruction!")
        sys.exit(0)
    elif wrongHit and not rightHit:
        print("You've killed yourself!")
        sys.exit(0)
    else:
        pass
  
def main():
    dot1, dot2 = makeDots()
    flatBlockList, tallBlockList = blockPositions(dot1, dot2)
    print('Player 1, try to hit the dot at ' + str(dot2))
    print('Player 2, try to hit the dot at ' + str(dot1))
    print('Exit the graph to continue\n')
    lastFxn = "x*0+30"
    firstGraph(dot1,dot2,flatBlockList, tallBlockList)
    turns = 1
    while True:
        turns += 1
        print('Player 1, what is your function?')
        lastFxn = graph(lastFxn, dot1, dot2, turns, flatBlockList, tallBlockList)
        win(lastFxn, dot2, dot1, flatBlockList, tallBlockList)
        print('Player 2, what is your function?')
        turns += 1
        lastFxn = graph(lastFxn, dot2, dot1, turns, flatBlockList, tallBlockList)
        win(lastFxn, dot1, dot2, flatBlockList, tallBlockList)

if __name__ == '__main__':
    main()
