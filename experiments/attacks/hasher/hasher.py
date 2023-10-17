from hashlib import blake2b
import os

class Hasher:
    def __init__(self, num_bins, rows, fixed_key=False):
        self.num_bins = num_bins
        self.rows = rows
        self.fp_key = bytes("fingerprint_key",'utf-8')
        if fixed_key:
            self.bin_key = bytes("bin_key",'utf-8')
        else:
            self.bin_key = os.urandom(16)

    def fpbhash(self,x):
        x = bytes(str(x), 'utf-8')
        hfp = blake2b(key=self.fp_key,digest_size=8)
        hfp.update(x)
        fphash = int.from_bytes(hfp.digest(),'big')
        hv = [fphash]
        for index in range(1,self.rows+1):
            bindex = bytes(str(index), 'utf-8')
            hbin = blake2b(key=self.bin_key,digest_size=16)
            hbin.update(bindex)
            hbin.update(x)
            bhash = int.from_bytes(hbin.digest(),'big')
            hv.append(bhash % self.num_bins)
        return hv
