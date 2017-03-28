# import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set_style("white")

# index = ['25', '26', '27']
# count = [10, 50, 22]
# phase = [0.9, 2.2, 1.2]
# rank  = [0, 2, 1]
# # 
# rank_classes = {0:"Ph<1", 1:"1<Ph<1.2", 2:"Ph>=1.2"}

# pal = sns.cubehelix_palette(len(index)) 
# cmp = mpl.colors.LinearSegmentedColormap.from_list('my_list', pal,\
#                                                     N=len(index))
# plot = plt.scatter(index, count, c=range(len(index)), cmap=cmp)
# plt.clf()
# plt.colorbar(plot)
# sns.barplot(x=index, y=count, palette=np.array(pal)[rank])
# sns.despine()

# plt.show()



# import matplotlib as mpl
# import matplotlib.pyplot as plt

# min, max = (-40, 30)
# step = 10

# # Setting up a colormap that's a simple transtion
# mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['blue','red'])

# # Using contourf to provide my colorbar info, then clearing the figure
# Z = [[0,0],[0,0]]
# levels = range(min,max+step,step)
# CS3 = plt.contourf(Z, levels, cmap=mymap)
# plt.clf()

# # Plotting what I actually want
# X=[[1,2],[1,2],[1,2],[1,2]]
# Y=[[1,2],[1,3],[1,4],[1,5]]
# Z=[-40,-20,0,30]
# for x,y,z in zip(X,Y,Z):
#     # setting rgb color based on z normalized to my range
#     r = (float(z)-min)/(max-min)
#     g = 0
#     b = 1-r
#     plt.plot(x,y,color=(r,g,b))
# plt.colorbar(CS3) # using the colorbar info I got from contourf
# plt.show()


import matplotlib.pyplot as plt
import matplotlib as mpl

# cmap = mpl.cm.cool
cmap = mpl.colors.ListedColormap(["#1240ab", "#26499d", "#3a528e", "#4d5b80", "#616372", "#756c64", "#887555", "#9c7e47", "#b08739", "#c4902b", "#d7981c", "#eba10e", "#ffaa00"])
norm = mpl.colors.Normalize(vmin=-1, vmax=1)

fig = plt.figure(figsize=(8, 3))
ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,norm=norm, orientation='horizontal')

fig = plt.gcf()
fig.canvas.set_window_title('color bar')

plt.show()




















