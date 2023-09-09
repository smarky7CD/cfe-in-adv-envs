import sys, os
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from hasher import Hasher
import math 


class CK:

    """
    This CK version implements flags.
    """

    def __init__(self,m,k,psi,fixed_key=False):
        self.m = m
        self.k = k
        self.psi = psi
        self. N = 0
        self.h = Hasher(m,k,fixed_key)
        self.M = [[0]*self.m for _ in range(self.k)]
        self.A = [[[-1,0]]*self.m for _ in range(self.k)] 
        
    def up(self, x):
        self.N += 1
        hv = self.h.fpbhash(x)
        fpx,p = hv[0], hv[1:]
        for i in range(self.k):            
            self.M[i][p[i]]+=1
            fpa,cnta = self.A[i][p[i]]
            # Case 1
            if cnta == 0:
                self.A[i][p[i]] = [fpx,1]
            # Case 2
            elif fpx == fpa:
                self.A[i][p[i]][1] = (cnta+1)  
            # Case 3
            else:
                self.A[i][p[i]][1] = (cnta-1)
                if self.A[i][p[i]][1] == 0:
                    self.A[i][p[i]][1] = 1
                    self.A[i][p[i]][0] = fpx
      
    def qry(self, x):
        theta1 = math.inf
        theta2 = math.inf
        cntUBx = self._qryCMS(x)
        cntLBx = self._qryHK(x)
        delta = math.inf
        flag = False
        if cntUBx == cntLBx:
            return cntUBx, flag
        hv = self.h.fpbhash(x)
        fpx,p = hv[0], hv[1:]
        for i in range(self.k):
            if self.A[i][p[i]][0] == -1:
                return 0, flag
            if self.A[i][p[i]][0] != fpx:
                theta1 = min(theta1, ((self.M[i][p[i]] - self.A[i][p[i]][1] + 1)/2))
                delta = min(delta, ((self.M[i][p[i]] - self.A[i][p[i]][1] + 1)/2))
            else:
                theta2 = min (theta2, self.A[i][p[i]][1] + ((self.M[i][p[i]] - self.A[i][p[i]][1])/2))
                delta = min(delta, ((self.M[i][p[i]] - self.A[i][p[i]][1])/2))
        cntUBx_est = min(cntUBx, theta1, theta2)
        if delta >= self.psi * self.N:
            flag = True
        return int(cntUBx_est), flag

    def _qryCMS(self,x):
        hv = self.h.fpbhash(x)
        _,p = hv[0], hv[1:]
        return min([self.M[i][p[i]] for i in range(self.k)])
    
    def _qryHK(self,x,fpx=-1):
        hv = self.h.fpbhash(x)
        fpx,p = hv[0], hv[1:]
        return max([self.A[i][p[i]][1] if self.A[i][p[i]][0] == fpx else 0 for i in range (self.k)])


