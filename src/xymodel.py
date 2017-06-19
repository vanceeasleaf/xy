# -*- coding: utf-8 -*-
# @Author: YangZhou
# @Date:   2017-06-19 14:03:52
# @Last Modified by:   YangZhou
# @Last Modified time: 2017-06-19 21:57:18

import numpy as np
import random


class xymodel(object):

    def __init__(self, SIZE, T, J=1, h=0):
        self.SIZE = SIZE
        self.J = J
        self.T = float(T)
        self.h = h
        self.m = np.zeros(SIZE * SIZE, int)
        self.m.shape = (SIZE, SIZE)
        self.E = 0.0
        self.cos = dict([(i * 5, (np.cos(i * 5 / 180.0 * 3.1415926)))
                         for i in range(0, 72)])
        self.be = dict([(i * 5, np.exp(self.cos[i * 5] / T))
                        for i in range(0, 72)])
        self.E = self.E0(self.m)
        self.sts = 0
        self.change = 0
        self.cutoff = 0.5
        # os.system('rm -r ./data/%.3f.dat'%self.T)

    def MCstep(self, N=1):
        f = open('./data/%.3f.dat' % self.T, 'w')
        output = ""
        for i in range(0, N):
            if self.change / float(self.sts + 1) <= 0.5:
                self.cutoff = self.cutoff * 0.8
            else:
                self.cutoff = 1 - (1 - self.cutoff) * 0.8
            self.sts = 0
            self.change = 0
            if i % 1 == 0:
                h1 = sum(sum(np.cos(self.m * 3.14 / 180.0))) / float(
                    self.SIZE * self.SIZE)
                h2 = sum(sum(np.sin(self.m * 3.14 / 180.0))) / float(
                    self.SIZE * self.SIZE)
                h3 = self.E / float(self.SIZE * self.SIZE)
                output += "%f\t%f\t%f\n" % (h1, h2, h3)
            for x in range(0, self.SIZE):
                for y in range(0, self.SIZE):
                    self.step(x, y)
        f.write(output)

    def E0(self, m):
        e0 = 0.0
        SIZE = self.SIZE
        J = self.J
        for x in range(0, SIZE):
            for y in range(0, SIZE):
                factor = y % 2 * 2 - 1
                neighbours = np.array([
                    m[x][(y + 1) % SIZE], m[x][(y - 1) % SIZE],
                    m[(x + 1) % SIZE][y], m[(x - 1) % SIZE][y],
                    m[(x - factor) % SIZE][(y - 1) % SIZE],
                    m[(x - factor) % SIZE][(y + 1) % SIZE]
                ])
                neighbours = (neighbours - m[x][y]) % 360
                e0 = e0 + sum([self.cos[i] for i in neighbours]) * J * (-1)

        return e0 / 2

    def step(self, x, y):
        SIZE = self.SIZE
        J = self.J

        factor = y % 2 * 2 - 1
        neighbours = np.array([
            self.m[x][(y + 1) % SIZE], self.m[x][(y - 1) % SIZE],
            self.m[(x + 1) % SIZE][y], self.m[(x - 1) % SIZE][y],
            self.m[(x - factor) % SIZE][(y - 1) % SIZE],
            self.m[(x - factor) % SIZE][(y + 1) % SIZE]
        ])

        jump = random.randint(
            1, int(35 * self.cutoff) + 1) * 5 * random.choice([1, -1])

        diff0 = (neighbours - self.m[x][y]) % 360
        diff1 = (neighbours - self.m[x][y] - jump) % 360

        p = np.prod([self.be[i] for i in diff1]) / \
            np.prod([self.be[i] for i in diff0])

        self.sts += 1
        if random.random() < p:
            self.change += 1
            self.m[x][y] = (self.m[x][y] + jump) % 360
            c = sum([self.cos[i] for i in diff0]) * J * (-1)
            self.E = self.E + (sum([self.cos[i] for i in diff1]) *
                               J * (-1) - c)

        # print jump
        # print self.E,self.E0(self.m)
