#%%
import matplotlib.pyplot as plt
import numpy as np
import os


def get_heavyXpercentcount(data, X=50):
    heavyXpercent = {}
    for name, dataset in data.items():
        topXprecent=0
        i=0
        for item in dataset['Count']:
            topXprecent += item
            i+=1
            if dataset['Count'].sum()*X/100.0 <= topXprecent:
                break
        heavyXpercent[name] = i
    return heavyXpercent


#Change the cwd to this file d. 
os.chdir(os.path.dirname(os.path.realpath(__file__)))
filename=os.path.basename(os.path.realpath(__file__)) 
filename = filename.split('.')[0] #Remove file extension.
filename = filename.split('plots')[0] #Remove plots extension if any.

plots_folder = 'plots'+os.sep
os.makedirs(plots_folder, exist_ok=True) 


colors = {'retail': '#084b83', 'novel': '#bf0603', 'kosarak': '#6db6b3'}
percents = [20,25,30,35]

#True freq.
retail = np.genfromtxt('../retail/retail_stream_info.csv', delimiter=',', names=True)
novel = np.genfromtxt('../novel/novel_stream_info.csv', delimiter=',', names=True)
kosarak = np.genfromtxt('../kosarak/kosarak_stream_info.csv', delimiter=',', names=True)

true_data = {'retail': retail, 'novel': novel, 'kosarak': kosarak}
heavypercent = {}
for X in percents:
    heavypercent[X] = get_heavyXpercentcount(true_data,X=X)
# %%
for name, dataset in true_data.items():

    title = 'Stream: '+name
    
    plt.rcParams["figure.facecolor"] = "w"
    plt.title(title, fontsize=7, color=colors[name])
    plt.plot(dataset['Count'][:heavypercent[percents[-1]][name]], color=colors[name], linewidth=0, markersize=2, marker='.')
    print(heavypercent[percents[-1]][name])
    
    vlines_locs = [v[name]-1 for (key,v) in heavypercent.items()]
    plt.vlines(vlines_locs, 0, int(dataset['Count'][:heavypercent[percents[-1]][name]][0]), color='firebrick', linewidth=1, linestyles='dashed')

    plt.tick_params(axis='x', labelsize=9)   
    plt.xticks(vlines_locs, [str(v[name])+'items' for (key,v) in heavypercent.items()],fontsize=3, rotation=45)
    plt.xlabel(str(max(percents))+"% of the stream PM",fontsize=8)
    plt.ylabel("Frequency")
    plt.ticklabel_format(axis='y', style='sci')
    
    plt.savefig(plots_folder+name+'_percents_'+str([str(p) for p in percents])+'.png', dpi=400)
    plt.clf()


# %%
