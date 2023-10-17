import sys, os, random, math
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from ck import CK
from hasher import Hasher


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

# ck attack
def ck_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_CK = CK(m,k,0.0012,fixed_key=True)
    cover, q_H, len_I = find_cover_hash(m,k,2,x)
    attack_insertions = 0
    while attack_insertions < q_U:
        for e in cover:
            cfe_CK.up(e)
        attack_insertions += len(cover)
    x_f,fr = cfe_CK.qry(x)
    if fr == True: 
        frx = 1
    else:
        frx = 0
    frc = 0
    for e in cover: 
        _, fre = cfe_CK.qry(e)
        if fre == True:
            frc += 1
    print(f"{q_H}, {len_I}, {len(cover)}, {x_f}, {frx}, {frc}")
    return q_H, len_I, len(cover), x_f, frx, frc

def run_trials(trials, attack, params):
    q_H_L = []
    len_I_L = []
    len_c_L = []
    x_f_L = []
    frx_L = []
    frc_L = [] 
    for i in range(trials):
        print(f"Trial {i}")
        q_H, len_I, len_c, x_f, frx, frc = attack(*params)
        q_H_L.append(q_H)
        len_I_L.append(len_I)
        len_c_L.append(len_c)
        x_f_L.append(x_f)
        frx_L.append(frx)
        frc_L.append(frc)
    print("\n\nAvg q_H, Avg |I|, Avg |C|, Avg Err, x Flags Raised, Cover Flags Raised")
    print(f"{sum(q_H_L)/trials}, {sum(len_I_L)/trials}, {sum(len_c_L)/trials}, {sum(x_f_L)/trials}, {sum(frx_L)/trials}, {sum(frc_L)/trials}")
    return sum(q_H_L)/trials, sum(len_I_L)/trials, sum(len_c_L)/trials, sum(x_f_L)/trials, {sum(frx_L)/trials}, {sum(frc_L)/trials}



if __name__ == "__main__":
    print("public, public: q_U=2^16, trials=100")
    print("CK: m=1024, k=4, psi=0.0012")
    run_trials(100, ck_attack, (1024,4,2**16))
  

"""
Results
Avg q_H, Avg |I|, Avg |C|, Avg Err, x Flags Raised, Cover Flags Raised
14428.44, 3607.11, 7.99, 8203.71, 1.0, 0.0
"""