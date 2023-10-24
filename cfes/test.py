import sys, os
sys.path.extend([f'{item[0]}' for item in os.walk(".") if os.path.isdir(item[0])])

from ck import CK
from cms import CMS
from hk import HK

import matplotlib.pyplot as plt
import numpy as np

cfe_ck = CK(341,2)
cfe_cms = CMS(512,4)
cfe_hk = HK(256,4)

cfe_ck.up("test")
cfe_cms.up("test")
cfe_hk.up("test")

ckq = cfe_ck.qry("test")
cmsq = cfe_cms.qry("test")
hkq = cfe_hk.qry("test") 

print(f"CK test qry is {ckq}")
print(f"CMS test qry is {cmsq}")
print(f"HK test qry is {hkq}")

plt.style.use('_mpl-gallery')

# make the data
np.random.seed(3)
x = 4 + np.random.normal(0, 2, 24)
y = 4 + np.random.normal(0, 2, len(x))
# size and color:
sizes = np.random.uniform(15, 80, len(x))
colors = np.random.uniform(15, 80, len(x))

# plot
fig, ax = plt.subplots()

ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))

plt.show()