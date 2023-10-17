import sys, os, random, math
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from ck import CK
from cms import CMS 
from hk import HK

# cms attack
def cms_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_CMS = CMS(m,k)
    cover = set()
    found = False
    I = []
    iI = len(I)
    a = cfe_CMS.qry(x)
    q_Up = 0
    q_Q = 1
    while not found:
        if q_Up >= q_U:
                x_f = cfe_CMS.qry(x)
                return iI, q_Up, q_Q, len(cover), x_f 
        y = random.randint(0,4294967296)
        if y == x or y in I:
            pass
        else:
            q_Up += 1
            I.append(y)
            cfe_CMS.up(y)
            a_p = cfe_CMS.qry(x)
            q_Q += 1
            if a_p != a:
                cover.add(y)
                found = True
    iI = len(I)
    for _ in range(k-1):
        #MinUncover algorithm inlined
        b_p = a_p - 1
        while a_p != b_p:
            if q_Up - len(cover) + 1 > q_U:
                x_f = cfe_CMS.qry(x)
                return iI, q_Up, q_Q, len(cover), x_f 
            b_p = a_p
            for y in cover:
                cfe_CMS.up(y)
                q_Up += 1
            a_p = cfe_CMS.qry(x)
            q_Q += 1
        a = a_p
        for y in I:
            if q_Up >= q_U:
                x_f = cfe_CMS.qry(x)
                return iI, q_Up, q_Q, len(cover), x_f 
            cfe_CMS.up(y)
            q_Up += 1
            a_p = cfe_CMS.qry(x)
            q_Q += 1
            if a_p != a:
                cover.add(y)
                I.remove(y)
                break
    q_Ur = q_Up
    while q_Up < q_U:
        for e in cover:
            cfe_CMS.up(e)
        q_Up += len(cover)
    x_f = cfe_CMS.qry(x)
    return iI, q_Ur, q_Q, len(cover), x_f 

# hk attack
def get_t(k,q_U,d=0.9,p=1/2**128):
    # k \times (q_U choose t) d^{t(t+1)/2} \leq k \times q_U^t d^{t(t+1)/2} \leq p
    a  = math.log(d) #d < 1 -> a < 1 -> quadratic function opens downward
    b  = math.log(d) + 2*math.log(q_U)
    c = - 2 * (math.log(p/k))
    
    x_1 = min((-b + math.sqrt(b**2 - (4*a*c))) / (2*a), (-b - math.sqrt(b**2 - (4*a*c))) / (2*a))
    x_2 = max((-b + math.sqrt(b**2 - (4*a*c))) / (2*a), (-b - math.sqrt(b**2 - (4*a*c))) / (2*a))
    if x_1 > 1 or x_2 < 1: t = 1
    elif x_2 > 1: t = math.ceil(x_2)
    return t

def hk_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_HK = HK(m,k)
    t = get_t(k, q_U)
    cover = set()
    I = set()
    cfe_HK.up(x)
    x_ins = 1
    q_Up = 1
    q_Q = 0
    for _ in range(k):
        # reintro loop
        reintro = False
        while not reintro:
            if q_Up >= q_U:
                x_f = cfe_HK.qry(x)
                return len(I), q_Up, q_Q, len(cover), x_ins - x_f
            cfe_HK.up(x)
            x_ins += 1
            q_Up += 1
            a = cfe_HK.qry(x)
            q_Q += 1
            if a > 0:
                reintro = True
        found = False
        while not found:
            if q_Up >= q_U:
                    x_f = cfe_HK.qry(x)
                    return len(I), q_Up, q_Q, len(cover), x_ins - x_f
            y = random.randint(0,4294967296)
            if y == x or y in I:
                pass
            else:
                q_Up += 1
                I.add(y)
                cfe_HK.up(y)
                a = cfe_HK.qry(x)
                q_Q += 1
                if a == 0:
                    cover.add(y)
                    found = True
                    for _ in range(t):
                        cfe_HK.up(y)
                    q_Up += t
    q_Ur = q_Up
    while q_Up < q_U:
        cfe_HK.up(x)
        # for e in cover:
        #     cfe_HK.up(e)
        x_ins += 1
        q_Up += 1
    x_f = cfe_HK.qry(x)
    return len(I), q_Ur, q_Q, len(cover), x_ins - x_f


# ck attack
def ck_attack(m,k,q_U):
    x = random.randint(0,4294967296)
    cfe_CK = CK(m,k)
    cover = set()
    found = False
    I = []
    iI = len(I)
    a = cfe_CK.qry(x)[0]
    q_Up = 0
    q_Q = 1
    while not found:
        if q_Up >= q_U:
                x_f = cfe_CK.qry(x)[0]
                return iI, q_Up, q_Q, len(cover), x_f 
        y = random.randint(0,4294967296)
        if y == x or y in I:
            pass
        else:
            q_Up += 1
            I.append(y)
            cfe_CK.up(y)
            a_p = cfe_CK.qry(x)[0]
            q_Q += 1
            if a_p != a:
                cover.add(y)
                found = True
    iI = len(I)
    for _ in range((2*k)-1):
        #MinUncover algorithm inlined
        b_p = a_p - 1
        while a_p != b_p:
            if q_Up - len(cover) + 1 > q_U:
                x_f = cfe_CK.qry(x)[0]
                return iI, q_Up, q_Q, len(cover), x_f 
            b_p = a_p
            for y in cover:
                cfe_CK.up(y)
                q_Up += 1
            a_p = cfe_CK.qry(x)[0]
            q_Q += 1
        a = a_p
        for y in I:
            if q_Up >= q_U:
                x_f = cfe_CK.qry(x)[0]
                return iI, q_Up, q_Q, len(cover), x_f 
            cfe_CK.up(y)
            q_Up += 1
            a_p = cfe_CK.qry(x)[0]
            q_Q += 1
            if a_p != a:
                cover.add(y)
                I.remove(y)
                break
    q_Ur = q_Up
    while q_Up < q_U:
        for e in cover:
            cfe_CK.up(e)
        q_Up += len(cover)
    x_f = cfe_CK.qry(x)[0]
    return iI, q_Ur, q_Q, len(cover), x_f 

def run_trials(trials, attack, params):
    iI_L = []
    Ur_L = []
    qQ_L = []
    len_c_L = []
    x_f_L = []
    for _ in range(trials):
        iI, q_Ur, q_Q, len_c, x_f = attack(*params)
        iI_L.append(iI)
        Ur_L.append(q_Ur)
        qQ_L.append(q_Q)
        len_c_L.append(len_c)
        x_f_L.append(x_f)
    print("Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err")
    print(f"{sum(iI_L)/trials}, {sum(Ur_L)/trials}, {sum(qQ_L)/trials}, {sum(len_c_L)/trials}, {sum(x_f_L)/trials}")
    return sum(iI_L)/trials, sum(Ur_L)/trials, sum(qQ_L)/trials, sum(len_c_L)/trials, sum(x_f_L)/trials


if __name__ == "__main__":
    print("private, private: q_U=2^20, trials=100")
    
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
private, private: q_U=2^20, trials=100
CMS: m=2048,k=4
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
4140.33, 17999.91, 11064.35, 3.99, 261116.16
CMS m=4096, k=8
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
11710.18, 44134.92, 35332.18, 7.99, 127029.66
CK: m=682,k=4
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
2363.96, 49817.74, 14141.75, 7.96, 130796.69
CK m=1365, k=8
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
6119.52, 94646.69, 37343.46, 15.93, 63776.52
HK: m=1024, k=4
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
8695.45, 9776.52, 8699.52, 4.0, 1038804.55
HK: m=2048, k=8
Avg |I|, Avg rs. ins., Avg Q, Avg |C|, Avg Err
38990.34, 61401.06, 59253.44, 7.98, 1007439.04
"""