import time
import random
import copy

SIZE = 12
DEPTH = 4

def draw_field(field):
	for i in range(0,SIZE):
		for j in range(0,SIZE):
			print field[i][j],
		print


def move(field, color):
	orig = field[0][0]
	do_move(field, color, orig, 0, 0)
	count = 0
	for i in range(0,SIZE):
		for j in range(0,SIZE):
			if field[i][j] == -1: 
				field[i][j] = color
				count += 1
	return count

	
def do_move(field, nc, oc, x, y):
	i = x
	field[x][y] = -1
	if (x < SIZE-1 and field[x+1][y] == oc):
		do_move(field, nc, oc, x+1, y)
	if (y < SIZE-1 and field[x][y+1] == oc):
		do_move(field, nc, oc, x, y+1)
	if (x > 0 and field[x-1][y] == oc):
		do_move(field, nc, oc, x-1, y)
	if (y > 0 and field[x][y-1] == oc):
		do_move(field, nc, oc, x, y-1)

def find_move(field, depth):
	if depth > DEPTH: return 0,0
	if is_done(field): return 0,1000
	max = -1
	midx = -1
	for c in range(0, 6):
		if c == field[0][0]: continue
		bfield = copy.deepcopy(field)
		r1 = move(bfield, c)
		nm, nr = find_move(bfield, depth+1)
		r = move(bfield, nm)
		if r+nr > max and r > r1:
			midx = c
			max = r+nr
	return midx, max
	
def is_done(field):
	for i in range(0,SIZE):	
		for j in range(0,SIZE):	
			if field[i][j] != field[0][0]:
				return False
	return True

def setup():
	random.seed(time.time())
	field = []
	for i in range(0,SIZE):
		field.append([])
		for j in range(0,SIZE):
			field[i].append(random.randint(0,5))

	

	#print step		
	#draw_field(field)
	
	return field

def solve_one_turn(field, size, depth):
        '''
        Search DEPTH levels deep and return the index to the next step.
        '''
        SIZE = size
        DEPTH = depth
        
        #draw_field(field)
        
        
        #m,r = find_move(field, 0)	
        #if m < 0 or m > 5 or field[0][0] == m:
        #        continue
        #move(field, m)
        
        return find_move(field, 0)[0]
#main()
