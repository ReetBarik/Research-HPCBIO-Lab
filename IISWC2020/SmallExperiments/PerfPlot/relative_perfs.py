import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import numpy as np
import seaborn as sns
import pandas as pd

#import os
#os.chdir('C:/Local/Coursework/Research-HPCBIO-Lab/GraphOrdering/HiPC2020/SmallExperiments/PerfPlot/')
# https://github.com/matplotlib/matplotlib/issues/5862#issuecomment-197330145
def fix_eps(fpath):
    """Fix carriage returns in EPS files caused by Arial font."""
    txt = b""
    with open(fpath, "rb") as f:
        for line in f:
            if b"\r\rHebrew" in line:
                line = line.replace(b"\r\rHebrew", b"Hebrew")
            txt += line
    with open(fpath, "wb") as f:
        f.write(txt)
        
def draw_lines(input_name):
    width = 5
    font_size = 50

    #set palette
    sns.set()
    sns.set_style("whitegrid", {'grid.color': '.5', 'grid.linestyle': u'-'})
    # palette = sns.cubehelix_palette(n_colors=3, start=0, rot=0.17, gamma=3.1, \
    #                             hue=0.9, light=0.9, dark=0.5, reverse = False, as_cmap=False)
    colors = ["#3498db", "#e74c3c", "#2ecc71", "#000000", "#3498db", "#e74c3c", "#2ecc71", "#3498db", "#e74c3c", "#2ecc71", "#3498db"]
    palette = sns.color_palette(colors)
    # palette = sns.hls_palette(6)
    sns.set_palette(palette)

    fig = plt.figure(figsize = (40, 17), dpi = 150)
    #fig = plt.figure(dpi=150)
    ax = plt.gca()
    fig.canvas.draw()

    df = pd.read_csv(input_name + '.csv', delimiter = ',')

    from itertools import cycle
    linecycler = cycle(["-","--",":","-."])
    markercycler = cycle(['o', 'v', 'D', 'd', 'p', 's'])

    np = df.shape[0] #rows
    ns = df.shape[1] #cols

    import numpy.matlib
    r = numpy.matlib.zeros(shape = [np, ns], dtype = float)
    df_mins = df.min(axis=1)
    for index, row in df.iterrows():
        r[index] = row / df_mins[index]
        #print r[index]
    #transpose the matrix to sort on each column
    r= numpy.transpose(numpy.sort(numpy.transpose(r)))

    lines = []
    pos = list(range(1, np + 1))
    # marker_style = dict(markersize=15)
    for i in range(0, ns):
        xs = numpy.repeat(r[:,i], 2).tolist()[0][1:]
        ys = [float(i) /np for i in numpy.repeat(pos, 2)[:-1]]
        if (sum(xs) > 0):
        	lines.append(ax.plot(xs, ys, linestyle = next(linecycler), fillstyle='none', \
                     marker = next(markercycler), \
                     markersize=15, linewidth=4))
        else:
            print('Boo')

    # associate each tick with thread number
    #ax.xaxis.grid(False)
    ax.tick_params(labelsize = 45)
    ax.set_xlabel('Performance Relative to the Best Algorithm', fontsize = font_size, labelpad=30)
    ax.set_ylabel('Fraction of datasets', fontsize = font_size)
    # associate each tick with thread number
    ax.set_ylim([0, 1.05])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])
    
    schemes = ['Natural', 'METIS', 'Degree Sort', 'RCM', 'Gorder', 'Grappolo', 'Random', 'Grappolo-RCM', 'Rabbit-Order', 'SlashBurn', 'ND']
    # set legend, exclude threadnumber
    leg = fig.legend(ax.lines, schemes, \
                    ncol = 1, frameon=True, fancybox = True, \
                    prop={'size':45}, shadow = False, framealpha=1.0, \
                    bbox_to_anchor = (0.79, 0.75)) #'xx-large')
    leg.get_frame().set_edgecolor('k')
    leg.get_frame().set_linewidth(1)	
    #plt.title(input_name + ' Arrangement', {'fontsize': 50})
    plt.show()
    fig.savefig(input_name + '.pdf', format = 'pdf', bbox_inches='tight')
    fig.savefig(input_name + '.eps', format = 'eps', bbox_inches='tight', dpi = fig.dpi)
    fix_eps(input_name + '.eps')

    return;

# change path accordingly
draw_lines('Average Linear')
# draw_lines('Maximum Linear')
# draw_lines('Bandwidth Avg')
# draw_lines('Time')
# draw_lines('Jugaad')
# draw_lines('Metis')
# draw_lines('SingleThread')
# draw_lines('SingleThreadIntel')
