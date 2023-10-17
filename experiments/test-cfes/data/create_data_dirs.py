import os

structs = ["ck","cms","hk"]
streams = ["kosarak","retail","novel"]
params = [["910x3","341x2"], ["2048x4","512x4"], ["1024x4","256x4"]]

for i,struct in enumerate(structs):
        for stream in streams:
            for p in params[i]:
                os.mkdir(f"{struct}_{p}_{stream}")
