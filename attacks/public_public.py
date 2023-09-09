import sys, os, random, math
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from ck import CK
from cms import CMS 
from hk import HK
from hasher import Hasher
from private_private import get_t as gt

# finds a cover set via hashing
def find_cover_hash(m,k,r,x):
    h = Hasher(m,k,fixed_key=True)
    cover = set()
    found = False
    I = set()
    tracker = [0]*k
    p = h.fpbhash(x)[1:]
    q_H = 0
    while not found:
        y = random.randint(0,4294967296)
        if y == x or y in I:
            pass
        else:
            q_H += k
            I.add(y)
            q = h.fpbhash(y)[1:]
            for i in range(k):
                if p[i] == q[i] and tracker[i] < r:
                    cover.add(y)
                    tracker[i] += 1
            if sum(tracker) == r*k:
                found = True
    return cover, q_H, len(I)

# cms attack
def cms_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_CMS = CMS(m,k,fixed_key=True)
    cover, q_H, len_I = find_cover_hash(m,k,1,x)
    attack_insertions = 0
    while attack_insertions < q_U:
        for e in cover:
            cfe_CMS.up(e)
        attack_insertions += len(cover)
    x_f = cfe_CMS.qry(x)
    return q_H, len_I, len(cover), x_f

def hk_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_HK = HK(m,k,fixed_key=True)
    cover, q_H, len_I = find_cover_hash(m,k,1,x)
    t = gt(k, q_U)
    # 100
    attack_insertions = t*len(cover)
    for e in cover:
        for _ in range(t):
            cfe_HK.up(e)
    x_ins = 0
    while attack_insertions < q_U:
        cfe_HK.up(x)
        attack_insertions += 1
        x_ins += 1
    x_f = cfe_HK.qry(x)
    return q_H, len_I, len(cover), x_ins - x_f

# ck attack
def ck_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_CK = CK(m,k,fixed_key=True)
    cover, q_H, len_I = find_cover_hash(m,k,2,x)
    attack_insertions = 0
    while attack_insertions < q_U:
        for e in cover:
            cfe_CK.up(e)
        attack_insertions += len(cover)
    x_f = cfe_CK.qry(x)[0]
    return q_H, len_I, len(cover), x_f

def run_trials(trials, attack, params):
    q_H_L = []
    len_I_L = []
    len_c_L = []
    x_f_L = []
    for _ in range(trials):
        q_H, len_I, len_c, x_f = attack(*params)
        q_H_L.append(q_H)
        len_I_L.append(len_I)
        len_c_L.append(len_c)
        x_f_L.append(x_f)
    print("Avg q_H, Avg |I|, Avg |C|, Avg Err")
    print(f"{sum(q_H_L)/trials}, {sum(len_I_L)/trials}, {sum(len_c_L)/trials}, {sum(x_f_L)/trials}")
    return sum(q_H_L)/trials, sum(len_I_L)/trials, sum(len_c_L)/trials, sum(x_f_L)/trials



if __name__ == "__main__":
    print("public, public: q_U=2^20, trials=100")

    print("CMS: m=2048,k=4")
    run_trials(100, cms_attack, (2048,4,2**20))
    print("CMS m=4096, k=8")
    run_trials(100, cms_attack, (4096,8,2**20))

    print("CK: m=682,k=4")
    run_trials(100, ck_attack, (682,4,2**20))
    print("CK m=1365, k=8")
    run_trials(100, ck_attack, (1365,8,2**20))

    print("HK: m=1024, k=4")
    run_trials(100, hk_attack, (1024,4,2**20))
    print("HK: m=2048, k=8")
    run_trials(100, hk_attack, (2048,8,2**20))

"""
public, public: q_U=2^16, trials=100
CMS: m=2048,k=4
Avg q_H, Avg |I|, Avg |C|, Avg Err
16933.4, 4233.35, 3.99, 263017.82
CMS m=4096, k=8
Avg q_H, Avg |I|, Avg |C|, Avg Err
88481.68, 11060.21, 8.0, 131072.0
CK: m=682,k=4
Avg q_H, Avg |I|, Avg |C|, Avg Err
9105.52, 2276.38, 7.96, 131821.0
CK m=1365, k=8
Avg q_H, Avg |I|, Avg |C|, Avg Err
50201.36, 6275.17, 15.97, 65667.1
HK: m=1024, k=4
Avg q_H, Avg |I|, Avg |C|, Avg Err
8146.4, 2036.6, 3.99, 1047502.69
HK: m=2048, k=8
Avg q_H, Avg |I|, Avg |C|, Avg Err
42827.52, 5353.44, 7.96, 1046434.76
"""