import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from hasher import Hasher

class CMS:

    def __init__(self,m,k,fixed_key=False):
        self.m = m
        self.k = k
        self.h = Hasher(m,k,fixed_key)
        self.M = [[0]*self.m for _ in range(self.k)]
        
    def up(self, x):
        hv = self.h.fpbhash(x)
        _,p = hv[0], hv[1:]
        for i in range(self.k):            
            self.M[i][p[i]]+=1
      
    def qry(self, x):
        hv = self.h.fpbhash(x)
        _,p = hv[0], hv[1:]
        return min([self.M[i][p[i]] for i in range(self.k)])
