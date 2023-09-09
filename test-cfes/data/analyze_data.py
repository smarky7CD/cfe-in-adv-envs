import os

def get_HEAVY(stream_file, stream_name, k):
    with open(stream_file, 'r') as f:
        lines = [line.rstrip() for line in f]

    freq = {} 
    N = 0
    for item in lines: 
        N+=1
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1

    sfreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    HEAVY_list = []
    HEAVY_set = set()

    with open(f"{stream_name}_{k}_heavy_items.csv", 'w') as wf:
        wf.write("Item,Count\n")
        for i in range(k):
            e = sfreq[i]
            wf.write(f"{e[0]},{e[1]}\n")
            HEAVY_list.append(e[0])
            HEAVY_set.add(e[0])

    return HEAVY_list, HEAVY_set

def get_exp_info(sd_name):
    info = sd_name.split('_')
    #structure, params, stream
    return info[0], info[1], info[2]

def get_est_freqs(data_file):
    with open(data_file) as f:
        lines = [line.rstrip() for line in f]
    est_freq_list = []
    est_freq_dict = {}
    for line in lines[1:]:
        elements = line.split(',')
        item = elements[0]
        est_freq = elements[2]
        est_freq_list.append((item,int(est_freq)))
        est_freq_dict[item] = int(est_freq)
    return sorted(est_freq_list,key = lambda x: x[1],reverse=True),est_freq_dict

def write_est_file(wf,est_freq_list):
    with open(wf,'w') as f:
        f.write("Item,EstFrq\n")
        for pair in est_freq_list:
            f.write(f"{pair[0]},{pair[1]}\n")

def write_all_est_files():
    rootdir = os.getcwd()
    for sub_dir in os.listdir(rootdir):
        full_sub_dir = os.path.join(rootdir, sub_dir)
        if os.path.isdir(full_sub_dir):
            structure, params, stream = get_exp_info(sub_dir)
            print(f"{structure} {params} {stream}")
            for trial in range(1000):
                with open(full_sub_dir + f"/{trial}.csv"):
                    est_freq_list,_ = get_est_freqs(full_sub_dir + f"/{trial}.csv")
                    write_est_file(full_sub_dir + f"/{trial}_est_freqs.csv",est_freq_list)


def main():

    novel_heavy_list, novel_heavy_set = get_HEAVY("../streams/novel_stream.txt", "novel", 22)
    retail_heavy_list, retail_heavy_set = get_HEAVY("../streams/retail_stream.txt", "retail", 22)
    kosarak_heavy_list, kosarak_heavy_set = get_HEAVY("../streams/kosarak_stream.txt", "kosarak", 20)

    rootdir = os.getcwd()
    for sub_dir in os.listdir(rootdir):
        full_sub_dir = os.path.join(rootdir, sub_dir)
        if os.path.isdir(full_sub_dir):
            structure, params, stream = get_exp_info(sub_dir)
            print(f"{structure} {params} {stream}")

            if stream == "novel":
                heavy_list = novel_heavy_list
                heavy_set = novel_heavy_set
            elif stream == "retail":
                heavy_list = retail_heavy_list
                heavy_set = retail_heavy_set
            else:
                heavy_list = kosarak_heavy_list
                heavy_set = kosarak_heavy_set

            heavy_match = []
            jaccard_i = []
            minimal_l = []
            percent_err = []
            
            for trial in range(1000):
                
                hm = 0
                ji = 0
                ml = 0
                pe = 0

                with open(full_sub_dir + f"/{trial}_est_freqs.csv", "r") as rf:
                    lines = [line.rstrip() for line in rf]
                lines = lines[1:]

                with open(full_sub_dir + f"/{trial}.csv", "r") as rf:
                    lines2 = [line.rstrip() for line in rf]
                lines2 = lines2[1:]

                # compute heavy match and ji
                hm_set = set()
                for i in range(len(heavy_list)):
                    chunks = lines[i].split(',')
                    element = chunks[0] 
                    hm_set. add(element)
                hm_int = heavy_set.intersection(hm_set)
                hm = len(hm_int)
                ji_un = heavy_set.union(hm_set)
                ji = len(ji_un)
                heavy_match.append(hm)
                jaccard_i.append(hm/ji)
                
                # compute minimal l 
                ml_set = set()
                last_freq = 0
                found = False
                for line in lines:
                    if not found:
                        chunks = line.split(',')
                        element = chunks[0]
                        last_freq = chunks[1]
                        ml_set.add(element)
                        if heavy_set.issubset(ml_set):
                            found = True
                    else:
                        chunks = line.split(',')
                        element = chunks[0]
                        freq = chunks[1]
                        if last_freq == freq:
                            ml_set.add(element)
                        else:
                            break
                ml = len(ml_set)
                minimal_l.append(ml)

                # compute_pe
                for i in range(len(heavy_list)):
                    pe += float(lines2[i].split(',')[4])
                percent_err.append(pe/len(heavy_list))

            with open(full_sub_dir + f"/results.csv", 'w') as wf:
                wf.write("trial,heavy_match,jaccard_i,minimal_l,percent_error\n")
                print("trial,heavy_match,jaccard_i,minimal_l,percent_error")
                for i in range(1000):
                    wf.write(f"{i+1},{heavy_match[i]},{jaccard_i[i]},{minimal_l[i]},{percent_err[i]}\n")
                    print(f"{i+1},{heavy_match[i]},{jaccard_i[i]},{minimal_l[i]},{percent_err[i]}")
                wf.write(f"tot,{sum(heavy_match)/1000},{sum(jaccard_i)/1000},{sum(minimal_l)/1000},{sum(percent_err)/1000}\n")
                print(f"tot,{sum(heavy_match)/1000},{sum(jaccard_i)/1000},{sum(minimal_l)/1000},{sum(percent_err)/1000}\n\n")

def get_tot_data():
    wf = open("total_results.csv", 'w') 
    wf.write("structure,params,stream,avg heavy_match,avg jaccard_i,avg minimal_l\n")
    print("structure,params,stream,avg heavy_match,avg jaccard_i,avg minimal_l")
    rootdir = os.getcwd()
    for sub_dir in os.listdir(rootdir):
        full_sub_dir = os.path.join(rootdir, sub_dir)
        if os.path.isdir(full_sub_dir):
            structure, params, stream = get_exp_info(sub_dir)
            with open(full_sub_dir + "/results.csv", 'r') as rf:
                lines = [line.rstrip() for line in rf]
            tot_line = lines[-1]
            stats = tot_line.split(',')
            hm,ji,ml,pe = stats[1], stats[2], stats[3],stats[4]
            wf.write(f"{structure},{params},{stream},{hm},{ji},{ml},{pe}\n")
            print(f"{structure},{params},{stream},{hm},{ji},{ml},{pe}")
    wf.close()

                        
if __name__ == "__main__":
    print("novel")
    novel_heavy_list, novel_heavy_set = get_HEAVY("../streams/novel_stream.txt", "novel", 22)
    print("retail")
    retail_heavy_list, retail_heavy_set = get_HEAVY("../streams/retail_stream.txt", "retail", 22)
    print("kosarak")
    kosarak_heavy_list, kosarak_heavy_set = get_HEAVY("../streams/kosarak_stream.txt", "kosarak", 20)
    print("\n\n")

    write_all_est_files()
    main()
    get_tot_data()