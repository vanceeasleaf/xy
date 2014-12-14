#!/usr/bin/env python
#-*- coding:utf-8 -*-

import scipy
import random
import math
import sys,os



class Ising (object):
    def __init__(self,SIZE,T,J=1,h=0,ifrandom=0):
        self.SIZE = SIZE
        self.J = J
        self.T = float(T)
        self.h = h
        
        self.m = scipy.ones(SIZE * SIZE,int)
        self.m.shape = (SIZE,SIZE)
        if ifrandom != 0:
            for x in xrange(0,SIZE):
                for y in xrange(0,SIZE):
                    if random.random() > 0.5:
                        self.m[x][y] = self.m[x][y] * (-1)
            
        
        

        self.e = scipy.exp
        
        self.E = 0.0
        
        self.p = {
            -12 + h: self.e((-1)*(-12+h)/T),
            -8 + h: self.e((-1)*(-8+h)/T),
            -4 + h: self.e((-1)*(-4+h)/T),
            0 + h: self.e((-1)*(0+h)/T),
            4 + h: self.e((-1)*(4+h)/T),
            8 + h: self.e((-1)*(8+h)/T),
            12 + h: self.e((-1)*(12+h)/T),
        }
        
        self.E = self.E0(self.m)

    def E0(self,m):
        e0 = 0.0
        SIZE = self.SIZE
        J = self.J
        h = self.h
        for x in xrange(0,SIZE):
                for y in xrange(0,SIZE):
                    factor = y%2 * 2 - 1
                    links = m[x][(y + 1)% SIZE ] + m[x][(y - 1)% SIZE ] + m[(x+1)%SIZE][y] + m[(x-1)%SIZE][y] + m[(x-factor)%SIZE][(y-1)%SIZE] + m[(x-factor)%SIZE][(y+1)%SIZE]
                    e0 = e0 + (m[x][y] * (links * J + h) ) * (-1)
    
        return e0/2

    def step(self, x, y):
        SIZE = self.SIZE
        J = self.J
        h = self.h
        p = self.p
        
        factor = y%2 * 2 - 1
        links = self.m[x][(y + 1)% SIZE ] + self.m[x][(y - 1)% SIZE ] + self.m[(x+1)%SIZE][y] + self.m[(x-1)%SIZE][y] + self.m[(x-factor)%SIZE][(y-1)%SIZE] + self.m[(x-factor)%SIZE][(y+1)%SIZE]
        deltaH = (self.m[x][y] * 2 * (links * J + h)) 
        #p = e((-1)*deltaH/T) 
        #j = random.random()
        #print deltaH,p[deltaH],j
        #print deltaH
    
        if random.random() < p[deltaH]:
            self.m[x][y] = self.m[x][y] * (-1)
            self.E = self.E + deltaH

    def MCstep(self, N):    
    
        
            
        os.system('rm ./data/%.3f.dat'%self.T)
        f = open("data/%.3f.dat"%self.T,"w")
        output = ""
    
        for i in xrange(0,N):
    
            if i%1 == 0:
                output += "%f\t%f\n"%(sum(sum(self.m)) / float(self.SIZE * self.SIZE), self.E / float(self.SIZE * self.SIZE))    
            
            for x in xrange(0,self.SIZE):
                for y in xrange(0,self.SIZE):
                    self.step(x,y)
        f.write(output)
                
        
if __name__=="__main__":	
	a=Ising(SIZE=16,T=1,J=1,h=0,ifrandom=0)
	a.MCstep(30)




