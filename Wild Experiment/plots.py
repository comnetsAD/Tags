import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
from datetime import datetime
import matplotlib.ticker as ticker
from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter, MultipleLocator
import numpy as np
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib.ticker import FixedLocator, FuncFormatter
from numpy import ma
from statannotations.Annotator import Annotator


plt.rc('xtick', labelsize=13) 
plt.rc('ytick', labelsize=15) 
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

devices = ['Apple', 'Samsung', 'Combined']

palette_colors = sns.color_palette('tab10')
palette_dict = {device: color for device, color in zip(devices, palette_colors)}


# ###############################################
# # Time Sweep at 0.01 Km from 1 Minute to 1 Hour#
# ###############################################

df = pd.read_csv("./Data/No_HomeV3/10m_Time_Sweep_Probability_Visited5Min.csv")

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

df['Percentage'] = df['Percentage'].apply(lambda x: x*100)

df['Time'] = df['Time'].apply(lambda x: x/60)

df = df[~((df['User'] == 'Yasir') & (df['Country'] == 'UAE'))]

g = sns.lineplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, errorbar = None, legend = False)
# g = sns.scatterplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, legend = False)
g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_ylim((0, 90))
g.set_xlabel("Time (minutes)",fontsize = 15)
axs.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
g.legend().remove()
plt.grid()
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/Visited_10m_Time_Sweep_Probability.pdf")

plt.clf()


# # ###############################################
# # # Time Sweep at 0.5 Km from 1 Minute to 1 Hour#
# # ###############################################

df = pd.read_csv("./Data/No_HomeV3/500m_Time_Sweep_Probability_Visited5Min.csv")

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

df['Percentage'] = df['Percentage'].apply(lambda x: x*100)
df['Time'] = df['Time'].apply(lambda x: x/60)

df = df[~((df['User'] == 'Yasir') & (df['Country'] == 'UAE'))]

g = sns.lineplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, errorbar = None, legend = False)
# g = sns.scatterplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, legend = False)
g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_ylim((0, 90))
g.set_xlabel("Time (minutes)",fontsize = 15)
axs.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])
g.legend().remove()
plt.grid()
# g.legend(loc = 4, fontsize = 10)
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/Visited_500m_Time_Sweep_Probability.pdf")

plt.clf()



# # ###############################################
# # # Time Sweep at 5 Km from 1 Minute to 1 Hour#
# # ###############################################

df = pd.read_csv("./Data/No_HomeV3/5km_Time_Sweep_Probability_Visited5Min.csv")

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

df['Percentage'] = df['Percentage'].apply(lambda x: x*100)
df['Time'] = df['Time'].apply(lambda x: x/60)

df = df[~((df['User'] == 'Yasir') & (df['Country'] == 'UAE'))]

g = sns.lineplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, errorbar = None, ax = axs)
# g = sns.scatterplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, legend = False)
g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_ylim((0, 90))
g.set_xlabel("Time (minutes)",fontsize = 15)

axs.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90])

g.legend(loc = 4, fontsize = 13)

plt.grid()

plt.tight_layout(pad = 0.1)

fig.savefig("./Plots/No_HomeV3/Visited_5km_Time_Sweep_Probability.pdf")

plt.clf()



# # ###############################################
# # # Radii Sweep #
# # ###############################################

df = pd.read_csv("./Data/No_HomeV3/Radii_Sweep_Probability_Visited5Min_Upto3Hours.csv")

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

df['Percentage'] = df['Percentage'].apply(lambda x: x*100)
df['Time'] = df['Time'].apply(lambda x: x/60)

df = df.loc[df['Device'] == 'Samsung']

g = sns.lineplot(data = df, x = "Distance", y = "Percentage", hue = "Time",  ax = axs, palette = palette_colors, errorbar = None)
# g = sns.scatterplot(data = df, x = "Distance", y = "Percentage", hue = "Time", ax = axs, legend = False)
g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_ylim((0, 100))
g.set_xlim((0, 0.1))
g.set_xlabel("Radius (km) ",fontsize = 15)

axs.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

g.legend(loc = 4, fontsize = 13, title = 'Time (minutes)')

plt.grid()

plt.tight_layout(pad = 0.1)

fig.savefig("./Plots/No_HomeV3/Visited_5km_Radius_Sweep_Probability_upto3hours_Samsung.pdf")

plt.clf()



# # # ###########################################################################
# # # # Speed Bucket Percentages for Each Radius at 5 Minute Resolution Combined#
# # # ###########################################################################

rows = 1
cols = 5

distances = [0.01, 0.1, 0.5, 1.0, 5.0]

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

df = pd.read_csv("./Data/No_HomeV3/Speed_Bucket_Percentages_No_Yasir_UAE.csv")
df['Percentage'] = df['Percentage'].apply(lambda x: x*100)

pairs = [('Stationary', 'Pedestrian'), ('Pedestrian', 'Jogging'),('Jogging', 'Transit')]

axs.set(ylim = (0, 75))
g= sns.barplot(data = df, x = "Speed", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, errorbar = 'ci', capsize = 0.05, errwidth = 1,  errcolor = 'black')


annot = Annotator(axs, pairs, data = df, x = 'Speed', y = 'Percentage', order = ['Stationary', 'Pedestrian', 'Jogging', 'Transit']) 

annot.configure(test = 't-test_ind', text_format = 'star', loc = 'inside', verbose = 2)
annot.apply_test()
axs, test_results = annot.annotate()

g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_xlabel("")
g.set_ylim((0, 100))
plt.xticks(rotation=30)
g.legend().remove()
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/Speed_Bucket_Percentages_No_Yasir_UAE.png")

plt.clf()


# # # ###########################################################################
# # # # Time Bucket Percentages for Each Radius at 5 Minute Resolution Combined#
# # # ###########################################################################

# rows = 1
# cols = 5

# distances = [0.01, 0.1, 0.5, 1.0, 5.0]

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

# df = pd.read_csv("./Data/No_HomeV2/Time_Bucket_Percentages_Visited.csv")
# df['Percentage'] = df['Percentage'].apply(lambda x: x*100)

# axs.set(ylim = (0, 100))
# g= sns.barplot(data = df, x = "Time", y = "Percentage", hue = "Device", palette=palette_dict, ax = axs, errorbar = 'ci', capsize = 0.05, errwidth = 1,  errcolor = 'black')
# g.legend(loc = 2)
# plt.tight_layout(pad = 0.1)
# fig.savefig("./Plots/No_HomeV2/Finalized/Time_Bucket_Percentages_Combined.pdf")

pairs = [("Morning", "Lunch"), ("Lunch", "Afternoon"),("Afternoon", "Evening"),("Evening", "Night")]

axs.set(ylim = (0, 75))
total = pd.read_csv("./Data/No_HomeV3/Time_Hexagon_Bucket_Percentages_Visited_5MinResolution_No_YASIR_UAE.csv")
print(total.head())
total['Percentage'] = total['Percentage'].apply(lambda x : x * 100)
# total = total.loc[total['Buckets'] >= 5]

g = sns.barplot(data = total, x = "Time", y = "Percentage", ax = axs, hue = "Device", hue_order = ['Apple', 'Samsung', 'Combined'], errorbar = 'ci', capsize = 0.05, errwidth = 1,  errcolor = 'black')

annot = Annotator(axs, pairs, data = total, x = 'Time', y = 'Percentage', order = ['Morning', 'Lunch', 'Afternoon', 'Evening', 'Night']) 

annot.configure(test = 't-test_ind', text_format = 'star', loc = 'inside', verbose = 2)
annot.apply_test()
axs, test_results = annot.annotate()

g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_xlabel("")
g.set_ylim((0, 100))
g.legend().remove()
# plt.legend(loc = 2, fontsize = 10)
plt.xticks(rotation=30)
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/Time_Hexagon_Bucket_Percentages_Visited_5MinResolution_No_YASIR_UAE.png")
# plt.show()


# # # ###########################################################################
# # # # WeekdayWeekend Bucket Percentages for Each Radius at 5 Minute Resolution Combined#
# # # ###########################################################################

rows = 1
cols = 5

distances = [0.01, 0.1, 0.5, 1.0, 5.0]

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54), dpi = 300)

pairs = [("Weekday", "Weekend")]

df = pd.read_csv("./Data/No_HomeV3/Weekday_Hexagon_Bucket_Percentages_Visited_5MinResolution_No_YASIR_UAE.csv")
df['Percentage'] = df['Percentage'].apply(lambda x: x*100)

axs.set(ylim = (0, 75))
g= sns.barplot(data = df, x = "Time", y = "Percentage", hue = "Device", hue_order = ['Apple', 'Samsung','Combined'],palette=palette_dict, ax = axs, errorbar = 'ci', capsize = 0.05, errwidth = 1,  errcolor = 'black')
g.legend(loc = 2, fontsize =  13)

annot = Annotator(axs, pairs, data = df, x = 'Time', y = 'Percentage', order = ['Weekday', 'Weekend']) 

annot.configure(test = 't-test_ind', text_format = 'star', loc = 'inside', verbose = 2)
annot.apply_test()
axs, test_results = annot.annotate()

g.set_ylabel("Accuracy (%)", fontsize = 15)
g.set_xlabel("", fontsize = 15)
g.set_ylim((0, 100))
plt.xticks(rotation=30)
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/Weekday_Hexagon_Bucket_Percentages_Visited_5MinResolution_No_YASIR_UAE.png")

plt.clf()



def simplify_cdf(data):
	'''Return the cdf and data to plot
		Remove unnecessary points in the CDF in case of repeated data
		'''
	data_len = len(data)
	assert data_len != 0
	cdf = np.arange(data_len) / data_len
	simple_cdf = [0]
	simple_data = [data[0]]

	if data_len > 1:
		simple_cdf.append(1.0 / data_len)
		simple_data.append(data[1])
		for cdf_value, data_value in zip(cdf, data):
			if data_value == simple_data[-1]:
				simple_cdf[-1] = cdf_value
			else:
				simple_cdf.append(cdf_value)
				simple_data.append(data_value)
	assert len(simple_cdf) == len(simple_data)
	# to have cdf up to 1
	simple_cdf.append(1)
	simple_data.append(data[-1])

	return simple_cdf, simple_data




def cdfplot(data_in):
	"""Plot the cdf of a data array
		Wrapper to call the plot method of axes
		"""
	# cannot shortcut lambda, otherwise it will drop values at 0
	data = sorted(filter(lambda x: (x is not None and ~np.isnan(x)
									and ~np.isinf(x)),
						data_in))

	data_len = len(data)
	if data_len == 0:
		return

	simple_cdf, simple_data = simplify_cdf(data)
	return simple_data, simple_cdf



df = pd.read_csv("./Data/No_HomeV3/Density_Hexagon_3Bucket_500m_1HourResolution_Visited10Min.csv")

df['Percentage'] = df['Percentage'].apply(lambda x: x*100)

df = df.replace("Low Density", "Low density")
df = df.replace("Medium Density", "Medium density")
df = df.replace("High Density", "High density")

fig, axs = plt.subplots(1, 3, figsize = (4.54*3, 3.54*1), dpi = 300)



for j, density in enumerate(['Low density', 'Medium density', 'High density']):

	density_df = df.loc[df['Density'] == density]


	for i,device in enumerate(density_df['Device'].unique()):
		scores = density_df.loc[density_df['Device'] == device]['Percentage']
		simple_data, simple_cdf = cdfplot(scores)
		label = device
		axs.ravel()[j].plot(simple_data, simple_cdf, color=palette_dict[device], \
			linewidth=2, label=label)
		axs.ravel()[j].set_ylim((0, 1.0))
		axs.ravel()[j].set_xlim((-1, 101))
		axs.ravel()[j].grid()
		axs.ravel()[j].set_xlabel("Accuracy (%)", fontsize = 15)
		axs.ravel()[j].set_title(density, fontsize = 15)


axs.ravel()[0].set_ylabel("CDF", fontsize = 15) 
axs.ravel()[2].legend(loc = 2, fontsize = 13)
plt.rc('xtick', labelsize=13) 
plt.rc('ytick', labelsize=15) 
# plt.xlabel("Chance of a Hit")
# plt.ylabel("Likelihood of occurence")
plt.tight_layout(pad = 0.1)
fig.savefig("./Plots/No_HomeV3/CDF_3Buckets.pdf")

plt.clf()

