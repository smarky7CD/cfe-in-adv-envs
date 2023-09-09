import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from hasher import Hasher
import random 

class HK:

    def __init__(self,m,k,d=0.9,fixed_key=False):
        self.m = m
        self.k = k
        self.d = d
        self.h = Hasher(m,k,fixed_key)
        self.A = [[[-1,0]]*self.m for _ in range(self.k)] 
        
    def up(self, x):
        hv = self.h.fpbhash(x)
        fpx,p = hv[0], hv[1:]
        for i in range(self.k):            
            fpa,cnta = self.A[i][p[i]]
            # Case 1
            if cnta == 0:
                self.A[i][p[i]] = [fpx,1]
            # Case 2
            elif fpx == fpa:
                self.A[i][p[i]][1] = (cnta+1)  
            # Case 3
            else:
                r = random.random()
                if r <= self.d**cnta:
                    self.A[i][p[i]][1] = cnta-1
                    if self.A[i][p[i]][1] == 0:
                        self.A[i][p[i]][1] = 1
                        self.A[i][p[i]][0] = fpx
      
    def qry(self, x):
        hv = self.h.fpbhash(x)
        fpx,p = hv[0], hv[1:]
        return max([self.A[i][p[i]][1] if self.A[i][p[i]][0] == fpx else 0 for i in range (self.k)])

