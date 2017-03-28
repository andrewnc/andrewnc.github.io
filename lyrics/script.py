
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from nltk.sentiment.vader import SentimentIntensityAnalyzer

import color_data

def get_color(number):
	if number < x[0]:
		return colors[0]
	elif number >= x[0] and number < x[1]:
		return colors[0]
	elif number >= x[1] and number < x[2]:
		return colors[1]
	elif number >= x[2] and number < x[3]:
		return colors[2]
	elif number >= x[3] and number < x[4]:
		return colors[3]
	elif number >= x[4] and number < x[5]:
		return colors[4]
	elif number >= x[5] and number < x[6]:
		return colors[5]
	elif number >= x[6] and number < x[7]:
		return colors[6]
	elif number >= x[7] and number < x[8]:
		return colors[7]
	elif number >= x[8] and number < x[9]:
		return colors[8]
	elif number >= x[9] and number < x[10]:
		return colors[9]
	elif number >= x[10] and number < x[11]:
		return colors[10]
	elif number >= x[11] and number < x[12]:
		return colors[11]
	elif number >= x[12]:
		return colors[12]

def get_color_other(number):
	if number < x[0]:
		return colors_other[0]
	elif number >= x[0] and number < x[1]:
		return colors_other[0]
	elif number >= x[1] and number < x[2]:
		return colors_other[1]
	elif number >= x[2] and number < x[3]:
		return colors_other[2]
	elif number >= x[3] and number < x[4]:
		return colors_other[3]
	elif number >= x[4] and number < x[5]:
		return colors_other[4]
	elif number >= x[5] and number < x[6]:
		return colors_other[5]
	elif number >= x[6] and number < x[7]:
		return colors_other[6]
	elif number >= x[7] and number < x[8]:
		return colors_other[7]
	elif number >= x[8] and number < x[9]:
		return colors_other[8]
	elif number >= x[9] and number < x[10]:
		return colors_other[9]
	elif number >= x[10] and number < x[11]:
		return colors_other[10]
	elif number >= x[11] and number < x[12]:
		return colors_other[11]
	elif number >= x[12] and number < x[13]:
		return colors_other[12]
	elif number >= x[13] and number < x[14]:
		return colors_other[13]
	elif number >= x[14] and number < x[15]:
		return colors_other[14]
	elif number >= x[15] and number < x[16]:
		return colors_other[15]
	elif number >= x[16] and number < x[17]:
		return colors_other[16]
	elif number >= x[17] and number < x[18]:
		return colors_other[17]
	elif number >= x[18] and number < x[19]:
		return colors_other[18]
	elif number >= x[19]:	
		return colors_other[19]



# for year in years:
# 	print "<div class='row'><div class='col-md-3'><img src=\"songs_{}.png\"></div></div>".format(str(year))

def plot_alternative_time(save=False):
	av_c = []
	av = 0
	for i in range(len(color_data.c)):
		
		if(i!= 0 and i%100 == 0):
			av_c.append(av/100.)
			av = 0
		else:
			av += color_data.c[i]
		
	av_c_r = []
	for i in av_c:
		av_c_r.append(get_color_other(i))

	years = [x for x in range(1965, 2016)]

	ones = np.ones(len(years))

	barlist = plt.bar(years, ones, width=1)
	for i in range(len(barlist)):
		barlist[i].set_color(av_c_r[i])

	frame1 = plt.gca()
	plt.xlim(1965,2015)
	frame1.axes.get_yaxis().set_visible(False)
	plt.title("Sentiment of top 100 songs since 1965")

	if(save):
		plt.savefig("figure_2.png")
	else:
		plt.show()


def plot_whole_timeperiod(save=False):
	# Get the average color for every year
	av_c = []
	av = 0
	for i in range(len(color_data.c)):
		
		if(i!= 0 and i%100 == 0):
			av_c.append(av/100.)
			av = 0
		else:
			av += color_data.c[i]
		
	av_c_r = []
	for i in av_c:
		av_c_r.append(get_color(i))

	years = [x for x in range(1965, 2016)]

	ones = np.ones(len(years))

	barlist = plt.bar(years, ones, width=1)
	for i in range(len(barlist)):
		barlist[i].set_color(av_c_r[i])

	frame1 = plt.gca()
	plt.xlim(1965,2015)
	frame1.axes.get_yaxis().set_visible(False)
	plt.title("Sentiment of top 100 songs since 1965")

	if(save):
		plt.savefig("figure_1.png")
	else:
		plt.show()


def plot_individual_years():
	nums = [x for x in range(1,101)]
	ones_hun = np.ones(len(nums))
	years = [x for x in range(1965, 2016)]
	counter = 0
	for year in years:
		barlist = plt.bar(nums, ones_hun, width=1)
		for i in range(len(barlist)):
			barlist[i].set_color(color_data.c_r[i+counter])
		counter += 100
		frame1 = plt.gca()
		plt.xlim(1,101)
		frame1.axes.get_yaxis().set_visible(False)
		plt.title("Sentiment of top 100 songs {}".format(str(year)))

		plt.savefig("songs_{}.png".format(str(year)))

def plot_individual_years_bar():
	year = 1965
	for i in xrange(0,len(color_data.c),100):
		num = []
		for j in xrange(i,i+100):
			num.append(color_data.c[j])
		plt.scatter([x for x in range(100)],num)
		plt.title("Sentiment of top 100 songs {}".format(str(year)))
		plt.ylim(-1.5,1.5)
		plt.savefig("scatter_songs_{}.png".format(str(year)))
		plt.clf()
		year += 1


def get_summary_statistics(li):
	year = 1965
	summary_stats = {}
	for i in xrange(1,len(color_data.c),100):
		num = []
		for j in xrange(i,i+100):
			if j < 5101:
				num.append(color_data.c[j])
			else:
				break
		summary_stats[year] = num
		year += 1
	st = ""
	counter = 1
	s = summary_stats
	for year in s:
		if year == 1965:
			# st += "<div class='year-{}' style=\"display:block;\">year: {} <br/> average sentiment: {} <br/> 1 : {} by {} score: {} ---- 2 : {} by {} score: {} ---- 3 : {} by {} score: {} <br/></div>".format(year, year, np.sum(s[year][0:3])/len(s[year][0:3]), li[counter][1], li[counter][2], s[year][0], li[counter+1][1], li[counter+1][2], s[year][1], li[counter+2][1], li[counter+2][2], s[year][2])
			st += "<div class='year-{}' style=\"display:block;\">year: {} <br/> average sentiment: {} <br/></div>".format(year, year, np.sum(s[year])/len(s[year]))
		else:
			st += "<div class='year-{}' style=\"display:none;\">year: {} <br/> average sentiment: {} <br/></div>".format(year, year, np.sum(s[year])/len(s[year]))
			# st += "<div class='year-{}' style=\"display:none;\">year: {} <br/> average sentiment: {} <br/> 1 : {} by {} score: {} ---- 2 : {} by {} score: {} ---- 3 : {} by {} score: {} <br/></div>".format(year, year, np.sum(s[year][0:3])/len(s[year][0:3]), li[counter][1], li[counter][2], s[year][0], li[counter+1][1], li[counter+1][2], s[year][1], li[counter+2][1], li[counter+2][2], s[year][2])
		
		# build table
		mini = 0
		stres = ""
		for j in li[counter:counter+100]:
			stres += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(j[0],j[1],j[2],s[year][mini])
			mini += 1
		if year == 1965:
			print "<table class=\"table table-year-{}\"><thead><th>Rank</th><th>Title</th><th>Artist</th><th>Score</th></thead><tbody>{}</tbody></table>".format(year, stres)
		else:
			print "<table class=\"table table-year-{}\" style=\"display:none;\"><thead><th>Rank</th><th>Title</th><th>Artist</th><th>Score</th></thead><tbody>{}</tbody></table>".format(year, stres)
		counter += 100

	return st


def generate_table(li):

	for i in li:
		print "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(i[0],i[1],i[2],i[3])


# To do: Fix two main graphs to reflect data

def top_song(li):
	year = 1965
	summary_stats = {}
	for i in xrange(1,len(color_data.c),100):
		num = []
		for j in xrange(i,i+100):
			if j < 5101:
				num.append(color_data.c[j])
			else:
				break
		summary_stats[year] = num
		year += 1
	max_value = 0
	max_index = 0
	max_year = 0

	min_value = 10
	min_index = 10
	min_year = 10
	for key in summary_stats:
		for i, x in enumerate(summary_stats[key]):
			if x > max_value:
				max_value = x
				max_index = i
				max_year = key

			if x < min_value:
				min_value = x
				min_index = i
				min_year = key
	return max_year,max_value,max_index, min_year,min_value,min_index

def top_year(li):
	year = 1965
	summary_stats = {}
	for i in xrange(1,len(color_data.c),100):
		num = []
		for j in xrange(i,i+100):
			if j < 5101:
				num.append(color_data.c[j])
			else:
				break
		summary_stats[year] = num
		year += 1

	years = {}
	for i in summary_stats:
		years[i] = sum(summary_stats[i])/100.

	max_val = 0
	min_val = 10
	max_year = 0
	min_year = 0
	for i in years:
		if years[i] > max_val:
			max_val = years[i]
			max_year = i
		if years[i] < min_val:
			min_val = years[i]
			min_year = i

	return max_val,max_year,min_val,min_year



if __name__ == "__main__":

	# plt.plot(years, av_c)	
	df=pd.read_csv('info.csv', sep=',',header=None)
	li= np.array(df.values)


	# s = get_summary_statistics(li)
	
	# print s

	# s = SentimentIntensityAnalyzer()
	# s.polarity_scores(str(li[i][4]))['compound']
	# BLUE: 1240AB - 1196203
	# YELLOW: FFAA00 - 16755200

	# colors_rgb = ["rgb(18,64,171)", "rgb(38,73,157)", "rgb(58,82,142)", "rgb(77,91,128)", "rgb(97,99,114)", "rgb(117,108,100)", "rgb(136,117,85)", "rgb(156,126,71)", "rgb(176,135,57)", "rgb(196,144,43)", "rgb(215,152,28)", "rgb(235,161,14)", "rgb(255,170,0)"]
	# colors = ["#1240ab", "#26499d", "#3a528e", "#4d5b80", "#616372", "#756c64", "#887555", "#9c7e47", "#b08739", "#c4902b", "#d7981c", "#eba10e", "#ffaa00"]
	# colors = ["#f7fbff","#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#2171b5","#08519c","#08306b"]
	# colors_other = ["#440154","#39568C","#1F968B","#73D055","#481567","#33638D","#20A387","#95D840","#482677","#2D708E","#29AF7F","#B8DE29","#453781","#287D8E","#3CBB75","#DCE319","#404788","#238A8D","#55C667","#FDE725"]
	# colors_other = colors_other[::-1]
	# print len(colors_other)
	# x = np.linspace(-1,1,len(colors))
	# x = np.linspace(-1,1,len(colors_other))


	year, val, ind, min_year,min_value,min_index = top_song(li)
	for i in li:
		if i[3] == str(year):
			if i[0] == str(ind+1):
				i = np.append(i,val)
				print i
		if i[3] == str(min_year):
			if i[0] == str(min_index+1):
				i = np.append(i,min_value)
				print i

	# print top_year(li)
	# plot_alternative_time(False)
	# generate_table(li)
	# counter = 1
	# for i in range(1965,2016):
	# 	s = ""
	# 	for j in li[counter:counter+100]:
	# 		s += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(j[0],j[1],j[2])
	# 	print "<table class=\"table table-year-{}\"><thead><th>Rank</th><th>Title</th><th>Artist</th><th>Score</th></thead><tbody>{}</tbody></table>".format(i, s)
	# 	counter += 100

	# plot_whole_timeperiod()
	# plot_individual_years()
	# plot_individual_years_bar()
	# for i in range(1965, 2016):
		# print "<li class=\"link {}\">{}</li>".format(i,i)
		# print "$(\"."+str(i)+"\").click(function(){$(\".to_switch1\").attr('src','scatter_songs_"+str(i)+".png');$(\".to_switch2\").attr('src', 'songs_"+str(i)+".png');$(\"*[class^='year-']\").hide();$(\".table\").hide();$(\".table-year-"+str(i)+"\").show();$(\".year-"+str(i)+"\").show();})"



