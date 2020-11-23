import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import math
import folium.plugins
from folium.plugins import HeatMap

df=pd.read_csv('2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv', header="infer", low_memory=False)
df.dropna(subset=['Primary Fur Color'])
df.drop(labels=['Highlight Fur Color','Combination of Primary and Highlight Color'], axis=1, inplace = True)
df.replace(to_replace='Gray', value='dimgrey', inplace=True)
df.replace(to_replace='Cinnamon', value='rosybrown', inplace=True)
df.replace(to_replace='Black', value='black', inplace=True)

blk_sqrl=df[df['Primary Fur Color']=='black']
grey_sqrl=df[df['Primary Fur Color']=='dimgrey']
red_sqrl=df[df['Primary Fur Color']=='rosybrown']
am_sqrl=df[df['Shift']=='AM']
pm_sqrl=df[df['Shift']=='PM']

blk_nums, grey_nums, red_nums, am_nums, pm_nums=[blk_sqrl.iloc[:, 13:27].sum(), grey_sqrl.iloc[:, 13:27].sum(), 
red_sqrl.iloc[:, 13:27].sum(), am_sqrl.iloc[:, 13:27].sum(), pm_sqrl.iloc[:, 13:27].sum()]

act_dfs=[b_act, g_act, r_act, am_act, pm_act]
act_arrs=[]
for df in act_dfs:
    act_arrs.append(df.to_numpy(copy=True))
x=blk_sqrl.iloc[:,13:18].columns.values
colors=['black', 'dimgrey', 'rosybrown', 'gold', 'deepskyblue']
titles=['Black Squirrels', 'Grey Squirrels', 'Red Squirrels', 'Morning Squirrels', 'Afternoon Squirrels']

def obs_graph(arrs, x, colors, titles, axs):
    for ax, arr, color, title in zip(axs.flatten(), arrs, colors, titles):
        ax.bar(x, arr, color=color)
        ax.set_ylabel('Rel Likelihood Obs')
        ax.set_title(title)
        ax.set_xticklabels(x, rotation=90)

def level_graph(arrs, x_arr, colors, labels):
    for arr, x, color, label in zip(arrs, x_arr, colors, labels):
        ax.bar(x, arr, color=color, width=0.1, label=label)

fig, ax= plot.subplots(figsize=(10,5), sharey=True)
ax.set_ylabel('Rel Rate of Obs')
ax.set_title("Height of Squirrel")
xTickMarks=x_loc
ax.set_xticks(x_lst[0])
ax.set_xticklabels(x_loc, rotation=90)
col_colors=colors[3:]
arrs=loc_arrs[3:]
level_graph(arrs, x_lst, col_colors, col_labels)
leg=ax.legend()
plot.tight_layout()

def ttest_act(s1_act, s2_act, s1_cnt, s2_cnt, a=0.1):
    shared_freq=(s1_act+s2_act)/(s1_cnt+s2_cnt)
    shared_var=(s1_cnt+s2_cnt)*shared_freq*(1-shared_freq)/(s1_cnt*s2_cnt)
    difference_in_proportions = stats.norm(0, np.sqrt(shared_var))
    threshold=difference_in_proportions.ppf(1-a)
    diff=s1_act/s1_cnt-s2_act/s2_cnt
    p_val=1-difference_in_proportions.cdf(diff)
    return difference_in_proportions
    print('threshold={:2.3f}, diff={:2.3f}, p_value={:2.3f}'.format(threshold, diff, p_val))

fig,ax =plot.subplots(1, figsize=(10,5))
ttest_act(grey_nums['Chasing'], red_nums['Chasing'], grey_cnt, red_cnt)
x=np.linspace(-1,1,num=500)
difference_in_proportions=ttest_act(grey_nums['Chasing'], red_nums['Chasing'], grey_cnt, red_cnt)
diff=grey_nums['Chasing']/grey_cnt-red_nums['Chasing']/red_cnt
threshold=difference_in_proportions.ppf(1-0.1)
ax.plot(x, difference_in_proportions.pdf(x), linewidth=3, color='forestgreen')
ax.axvline(threshold, color='maroon')
ax.set_facecolor('floralwhite')
ax.fill_between(x, 
difference_in_proportions.pdf(x), where=(x >= diff), color='tan', alpha=0.7)
ax.set_xlim(-0.3,0.3)
ax.set_title('null hypothesis and p-value region')
ax.set_ylabel('Probability Density')
ax.set_xlabel('Probability of a grey and red squirrel chasing other squirrels assuming $H_0$');
plot.savefig('figs/graphs/chasing.png', bbox_inches = "tight")
