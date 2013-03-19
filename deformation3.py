import pygame, sys, os, random
from pygame.locals import * 
from math import *
import time
import random
 
pygame.init() 
clock = pygame.time.Clock()

screen_t = 500
screen_x = 2*screen_t
screen_y = screen_t
screen = pygame.display.set_mode((screen_x, screen_y))

n = 10
v_x = [[0 for i in range(n+1)] for j in range(n+1)]
v_y = [[0 for i in range(n+1)] for j in range(n+1)]
for i in range(0, n+1):
	for j in range(0, n+1):
		v_y[i][j] = 1.0*i/n
		v_x[i][j] = 1.0*j/n

density = [[0.5 for i in range(n)] for j in range(n)]
avg_density_now = 0.0

#---Random 1/0.5 assignment
for i in range(0, n/2):
	for j in range(0, n/2):
		if (random.random() >= 0.5):
			density[2*i][2*j] = 1.0
			density[2*i+1][2*j] = 1.0
			density[2*i][2*j+1] = 1.0
			density[2*i+1][2*j+1] = 1.0

#---Left/right bipartition
#for i in range(0, n):
#	for j in range(0, n/2):
#		density[i][j] = 1.0

#---Central dense square
#for i in range(n/4, 3*n/4):
#	for j in range(n/4, 3*n/4):
#		density[i][j] = 1.0

#---Central sparse square
#for i in range(0, n):
#	for j in range(0, n):
#		density[i][j] = 1.0
#for i in range(n/4, 3*n/4):
#	for j in range(n/4, 3*n/4):
#		density[i][j] = 0.5

#---Chessboard
#for i in range(0, n):
#	for j in range(0, n):
#		if ((i/5 + j/5) % 2 == 1):
#			density[i][j] = 1.0

#---Fine chessboard
#for i in range(0, n):
#	for j in range(0, n):
#		if ((i/2 + j/2) % 2 == 1):
#			density[i][j] = 1.0

def tr_area(xA, yA, xB, yB, xC, yC):
	ans = 0.5*fabs((xA-xC)*(yB-yA) - (xA-xB)*(yC-yA))
	return ans

def quad_area(xA, yA, xB, yB, xC, yC, xD, yD):
	ans = tr_area(xA, yA, xB, yB, xC, yC) + tr_area(xA, yA, xD, yD, xC, yC)
	return ans

def avg_density():
	vol1 = 0.0
	vol2 = 0.0
	for i in range(0,n+1):
		for j in range(0,n+1):
			x0 = v_x[i][j];		y0 = v_y[i][j]
			if (i>0) and (j>0):
				x1 = v_x[i-1][j];	y1 = v_y[i-1][j]
				x7 = v_x[i][j-1];	y7 = v_y[i][j-1]
				x8 = v_x[i-1][j-1];	y8 = v_y[i-1][j-1]
				vol1 = vol1 + quad_area(x0,y0,x7,y7,x8,y8,x1,y1)
				vol2 = vol2 + density[i-1][j-1]
			if (i>0) and (j<n):
				x1 = v_x[i-1][j];	y1 = v_y[i-1][j]
				x2 = v_x[i-1][j+1];	y2 = v_y[i-1][j+1]
				x3 = v_x[i][j+1];	y3 = v_y[i][j+1]
				vol1 = vol1 + quad_area(x0,y0,x1,y1,x2,y2,x3,y3)
				vol2 = vol2 + density[i-1][j]
			if (i<n) and (j<n):
				x3 = v_x[i][j+1];	y3 = v_y[i][j+1]
				x4 = v_x[i+1][j+1];	y4 = v_y[i+1][j+1]
				x5 = v_x[i+1][j];	y5 = v_y[i+1][j]
				vol1 = vol1 + quad_area(x0,y0,x3,y3,x4,y4,x5,y5)
				vol2 = vol2 + density[i][j]
			if (i<n) and (j>0):
				x5 = v_x[i+1][j];	y5 = v_y[i+1][j]
				x6 = v_x[i+1][j-1];	y6 = v_y[i+1][j-1]
				x7 = v_x[i][j-1];	y7 = v_y[i][j-1]
				vol1 = vol1 + quad_area(x0,y0,x5,y5,x6,y6,x7,y7)
				vol2 = vol2 + density[i][j-1]
	return vol2 / vol1

def local_densities(i,j):
	a = []
	x0 = v_x[i][j];		y0 = v_y[i][j]
	if (i>0) and (j>0):
		x1 = v_x[i-1][j];	y1 = v_y[i-1][j]
		x7 = v_x[i][j-1];	y7 = v_y[i][j-1]
		x8 = v_x[i-1][j-1];	y8 = v_y[i-1][j-1]
		dens = density[i-1][j-1] / quad_area(x0,y0,x7,y7,x8,y8,x1,y1)
		a.append(dens)
	if (i>0) and (j<n):
		x1 = v_x[i-1][j];	y1 = v_y[i-1][j]
		x2 = v_x[i-1][j+1];	y2 = v_y[i-1][j+1]
		x3 = v_x[i][j+1];	y3 = v_y[i][j+1]
		dens = density[i-1][j] / quad_area(x0,y0,x1,y1,x2,y2,x3,y3)
		a.append(dens)
	if (i<n) and (j<n):
		x3 = v_x[i][j+1];	y3 = v_y[i][j+1]
		x4 = v_x[i+1][j+1];	y4 = v_y[i+1][j+1]
		x5 = v_x[i+1][j];	y5 = v_y[i+1][j]
		dens = density[i][j] / quad_area(x0,y0,x3,y3,x4,y4,x5,y5)
		a.append(dens)
	if (i<n) and (j>0):
		x5 = v_x[i+1][j];	y5 = v_y[i+1][j]
		x6 = v_x[i+1][j-1];	y6 = v_y[i+1][j-1]
		x7 = v_x[i][j-1];	y7 = v_y[i][j-1]
		dens = density[i][j-1] / quad_area(x0,y0,x5,y5,x6,y6,x7,y7)
		a.append(dens)
	return a

def max_density():
	max_dens = 0
	first_time = 1
	for i in range(0,n+1):
		for j in range(0,n+1):
			a = local_densities(i,j)
			if first_time == 1:
				max_dens = max(a)
				first_time = 0
			else:
				max_dens = max(max_dens, max(a))
	return max_dens

def min_density():
	min_dens = 0
	first_time = 1
	for i in range(0,n+1):
		for j in range(0,n+1):
			a = local_densities(i,j)
			if first_time == 1:
				min_dens = min(a)
				first_time = 0
			else:
				min_dens = min(min_dens, min(a))
	return min_dens

def local_cost(i, j, dy, dx): #the local cost of purturbing the (i,j) point by (dy,dx)
	v_x[i][j] = v_x[i][j]+dx;
	v_y[i][j] = v_y[i][j]+dy
	a = local_densities(i,j)
	v_x[i][j] = v_x[i][j]-dx;
	v_y[i][j] = v_y[i][j]-dy
	return [min(a), max(a)]

def deform():
	j = random.randint(1, n-1)
	i = random.randint(1, n-1)
	cost_old = local_cost(i, j, 0.0, 0.0)
	dx = (random.random() - 0.5) / (200*n)
	dy = (random.random() - 0.5) / (200*n)
	cost_new = local_cost(i, j, dy, dx)
	if (min(cost_new) >= min(cost_old)) and (max(cost_new) <= max(cost_old)):
		v_x[i][j] = v_x[i][j] + dx
		v_y[i][j] = v_y[i][j] + dy

def show():
	screen.fill((0,0,0))
	for i in range(0,n):
		for j in range(0,n):
			x1 = screen_t*0.05+0.9*screen_t*j/n
			y1 = screen_t*0.05+0.9*screen_t*i/n
			x2 = screen_t*0.05+0.9*screen_t*(j+1)/n
			y2 = screen_t*0.05+0.9*screen_t*i/n
			x3 = screen_t*0.05+0.9*screen_t*(j+1)/n
			y3 = screen_t*0.05+0.9*screen_t*(i+1)/n
			x4 = screen_t*0.05+0.9*screen_t*j/n
			y4 = screen_t*0.05+0.9*screen_t*(i+1)/n
			if (density[i][j] == 1.0):
				pygame.draw.polygon(screen, (255,0,0), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 0)
			else:
				pygame.draw.polygon(screen, (0,255,0), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 0)
			pygame.draw.polygon(screen, (255,255,255), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 1)
			x1 = screen_t*0.05+0.9*screen_t*v_x[i][j] + screen_t
			y1 = screen_t*0.05+0.9*screen_t*v_y[i][j]
			x2 = screen_t*0.05+0.9*screen_t*v_x[i][j+1] + screen_t
			y2 = screen_t*0.05+0.9*screen_t*v_y[i][j+1]
			x3 = screen_t*0.05+0.9*screen_t*v_x[i+1][j+1] + screen_t
			y3 = screen_t*0.05+0.9*screen_t*v_y[i+1][j+1]
			x4 = screen_t*0.05+0.9*screen_t*v_x[i+1][j] + screen_t
			y4 = screen_t*0.05+0.9*screen_t*v_y[i+1][j]
			if (density[i][j] == 1.0):
				pygame.draw.polygon(screen, (255,0,0), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 0)
			else:
				pygame.draw.polygon(screen, (0,255,0), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 0)
			pygame.draw.polygon(screen, (255,255,255), ((x1,y1),(x2,y2),(x3,y3),(x4,y4)), 1)
	pygame.display.flip()
	return
	
def main():
	done=0
	while (done == 0):
#		clock.tick(10)
		show()
		avg_density_now = avg_density()
		print "avg =", avg_density_now, "max =", max_density(), "min =", min_density(), "ratio =", max_density()/min_density()
		for i in range(1,10000):
			deform()
		for event in pygame.event.get():
			if event.type == QUIT: 
				sys.exit(0) 
			elif event.type == KEYDOWN:
				if event.key == 27:
					done=1
	return

main()

