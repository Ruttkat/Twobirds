#!/usr/bin/env python
#
# todo: detect when *we* have no surviving moves.

import sys
import sqlite3 as db
import codecs
import cPickle as cP

#from copy import deepcopy
def deepcopy(twod): # faster
  return [x[:] for x in twod]

lang     = 'dict/twl'
CUTOFF   = 20 # only analyze the n longest words
SHORTEST = 3 # stop when the longest word is this long

BONI  = [0,0,0,0,1,3,5,8,10,12,14,16,18]
#        A B C D E F G H I J  K L M N O P Q R S T U V W X  Y Z
WORTH = [1,4,4,2,1,4,3,3,1,10,5,2,3,2,1,4,8,1,1,1,2,4,4,10,4,10]

nope, infile = sys.argv[0:2]
moves = sys.argv[2:]

conn = db.connect("%s.sqlite" % lang)
c    = conn.cursor()

lines   = [line.strip() for line in codecs.open("games/"+infile,'r','utf-8').read().strip().split("\n")]
golden  = [[l.isupper() for l in line] for line in lines]
letters = [[l.upper() for l in line] for line in lines]

def beginable(root):
  c.execute('select * from lastbits where bit = "%s" limit 1' % root)
  return c.fetchone() and True or False

def continuable(root):
  c.execute('select * from bits where bit = "%s" limit 1' % root)
  return c.fetchone() and True or False

def exists(root):
  c.execute('select * from words where word = "%s" limit 1' % root)
  return c.fetchone() and True or False

def startsat (y, x, sizey, sizex, board, root, chain):
  if (y,x) in chain: return []
  chain = chain + [(y,x)]

  found = []
  for dx in [-1,0,1]:
    for dy in [-1,0,1]:
      nx = x+dx
      ny = y+dy
      if (ny<0) or (nx<0) or (ny>=sizey) or (nx>=sizex):
        continue
      elif continuable(root):
        found = found + startsat(ny, nx, sizey, sizex, board, root+board[ny][nx], chain)

  if exists(root):
    return [(root, chain)]+found
  else:
    return found

def remove(board, word):
  for y,x in word[1]:
    board[y][x] = '.'
  return board

def shrink(board):
  shrinked = []
  vlen = 0
  for x in xrange(len(board[0])):
    letters = []
    for y in xrange(len(board)):
      if board[y][x] != '.':
        letters.append(board[y][x])
    v = len(letters)
    if v:
      if v > vlen: vlen = v
      shrinked.append(letters)

  for i,col in enumerate(shrinked):
    if len(col) < vlen:
      shrinked[i] = (['.'] * (vlen-len(col))) + col
 
  transposed = [list(i) for i in zip(*shrinked)]
  return transposed

def print_board(board):
  for y in board:
    for x in y:
      print x,
    print

def wordscore(word):
  bonus = BONI[len(word[0])] 
  score = sum([WORTH[ord(letter)-ord('A')] for letter in word[0]])
  extra = sum([(golden[x][y] and 10 or 0) for x,y in word[1]])
  score += bonus + extra
  return score

def solve (board):
  if not len(board): 
    return 25, ['-solved-']

  sizex   = len(board[0])
  sizey   = len(board)
  words   = []
  for y in xrange(sizey):
    for x in xrange(sizex):
      words += startsat(y,x,sizey,sizex,board,board[y][x],[])
  words = sorted(words, key=lambda x:wordscore(x), reverse=True)
  
  best  = []
  bestpoints = 0
  if len(words) and len(words[0][0]) >= SHORTEST:
    for word in words[0:CUTOFF]:
      print word[0], wordscore(word)
  else:
    best=['-endgame-']

  return bestpoints, best

for move in moves:
  # TODO:
  # identify move in board
  # remove move from board
  # shrink board
  pass

score, solution = solve(letters)
#print score
#print [w[0] for w in solution]

