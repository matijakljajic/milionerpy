# basic func imports
import random

# graph imports
import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt

def makegraph(opcije):
    t = random.randrange(42, 88)
    f1 = random.randrange(0,12)
    f2 = (100 - (t + f1)) // random.randrange(1,4)
    f3 = 100 - (t + f1 + f2)
    ti = 0
    for i in range(0, len(opcije)):
        if opcije[i][1] == 'T':
            ti = i

    if ti == 0:
        data = {'A':t, 'B':f1, 'C':f2, 'D':f3}
    elif ti == 1:
        data = {'A':f1, 'B':t, 'C':f2, 'D':f3}
    elif ti == 2:
        data = {'A':f1, 'B':f2, 'C':t, 'D':f3}
    else: data = {'A':f1, 'B':f2, 'C':f3, 'D':t}

    labels = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(4,4),facecolor='#1e2633')
    ax = fig.add_subplot(111)

    plt.bar(labels, values, color ='#ea8a00')
    ax.tick_params(axis='x', colors='#ea8a00')
    ax.tick_params(axis='y', colors='#ea8a00')
    ax.spines[['left','right','top','bottom']].set_color('#ea8a00')
    ax.set_facecolor('#1e2633')
    
    plt.savefig('resources/figure.png')
