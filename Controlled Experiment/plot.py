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
from matplotlib.lines import Line2D


plt.rc('axes', labelsize=15)
plt.rc('xtick', labelsize=15) 
plt.rc('ytick', labelsize=15)
plt.rcParams['hatch.linewidth'] = 0.2 
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

devices = ['Apple', 'Samsung', 'Combined']

palette_colors = sns.color_palette('tab10')[:3]
palette_dict = {device: color for device, color in zip(devices, palette_colors)}


rates = pd.read_csv("Hourly_Update_Rates.csv")
counts = pd.read_csv("D2_Device_Counts_Sorted.csv")


rates['Date'] = rates['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
rates['Date'] = rates['Date'].apply(lambda x: x.strftime('%H'))
rates['Date'] = rates['Date'].astype(str)


counts['Hour'] = counts['Hour'].apply(lambda x: datetime.strptime(str(x), '%H'))
counts['Hour'] = counts['Hour'].apply(lambda x: x.strftime('%H'))
counts['Hour'] = counts['Hour'].astype(str)


# counts = counts.loc[counts['Device'] != "Unknown"]

# counts = counts.sort_values(by = "Hour")
# rates = rates.sort_values(by = "Date")

counts = counts.rename(columns = {"Count" : "Device Count"})

fig, axs = plt.subplots(1, 1, figsize = (4.54*3, 3.54*1), dpi = 300)

hatches = ['//////' for i in range(24)]
hatches.extend('+++' for i in range(24))

axs.grid(color = '#DEDEDE', linestyle = '--', zorder = 3)

# Loop over the bars
ax2 = axs.twinx()


ax2.set_axisbelow(True)

g = sns.barplot(data = counts, x = "Hour", y = "Device Count", hue = "Device", hue_order = ['Apple', 'Samsung'], ax = axs, palette = palette_dict, edgecolor = 'black', errwidth = 0.5, errcolor = 'black')

print(len(g.patches))


for i,thisbar in enumerate(g.patches):
    thisbar.set_hatch(hatches[i])


g2 = sns.lineplot(data = rates, x = "Date", y = "Rate", hue = "Device", hue_order = ['Apple', 'Samsung'], palette = palette_colors, ax = ax2, sort = False, linewidth = 2, errorbar = 'sd')

g2.lines[0].set_linestyle("--")

ax2.set_ylim(bottom = 0, top = 24)
g.set_ylim(bottom = 0, top = 600)
g.set_ylabel("Device count")
g.set_xlabel("Time of day (hour)", fontsize = 15)
# axs.grid()


line = Line2D([0,1],[0,1],linestyle='--', color=palette_dict['Apple'], label = "AirTag")
line2 = Line2D([0,1],[0,1],linestyle='-', color=palette_dict['Samsung'], label = "SmartTag")

g2.legend(handles = [line,line2], title = "Update rate", loc = "upper right")

ax2.set_ylabel("Update rate")
# ax2.legend(loc = 'upper right', title = "Update rate")
g.legend(loc = 'upper left', title = "Number of devices")



plt.xticks(rotation = 30)

plt.tight_layout(pad = 0.1)

fig.savefig("Hourly_Update_Rates.png")

plt.clf()

#####################################################################################

categories = ["1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100","101-200","201-300","301-400","> 400"]
  

plt.rc('xtick', labelsize=13)

total = pd.read_csv("Rate_Count_Merged.csv")
hist_data= pd.read_csv("Count_Histogram.csv")

print(total.head())
print(hist_data.head())


total['Hour'] = total['Hour'].apply(pd.to_numeric)
total['Rate'] = total['Rate'].apply(pd.to_numeric)
total['Count'] = total['Count'].apply(pd.to_numeric)

total = total.sort_values(by = "Bucket")
total.Bucket = pd.Categorical(total.Bucket, categories=map(str, categories), ordered=True)
hist_data.Bucket = pd.Categorical(hist_data.Bucket, categories=map(str, categories), ordered=True)

hist_data = hist_data.sort_values(by = "Bucket")
# total = total.rename(columns = {"Count": "Device Count"})
# total = total[['Device', 'Rate', 'Device Count']]
# total = total.sort_values(by = "Count")

# print(hist_data.head())
# print(total.head())
# sns.set_context(rc = {'patch.linewidth': 2.5})

fig, axs = plt.subplots(1, 1, figsize = (4.54*3, 3.54*1), dpi = 300)
ax2 = axs.twinx()

g2 = sns.lineplot(data = total, x = "Bucket", y = "Rate", hue = "Device", palette = palette_dict, hue_order = ['Apple', 'Samsung'], ax = ax2, zorder = 10, linewidth = 2)

g2.lines[0].set_linestyle("--")

g = sns.barplot(data = hist_data, x = "Bucket", y = "NumOccur", hue = "Device", palette = palette_dict, hue_order = ['Apple', 'Samsung'], ax = axs, alpha = 0.8, order = ["1-10","11-20","21-30","31-40","41-50","51-60","61-70","71-80","81-90","91-100","101-200","201-300","301-400","> 400"], edgecolor = '#000000', zorder = -1)




print(len(g.patches))

hatches = ['////' for i in range(14)]
hatches.extend('++++' for i in range(14))

for i,thisbar in enumerate(g.patches):
    thisbar.set_hatch(hatches[i])


line = Line2D([0,1],[0,1],linestyle='--', color=palette_dict['Apple'], label = "AirTag")
line2 = Line2D([0,1],[0,1],linestyle='-', color=palette_dict['Samsung'], label = "SmartTag")

g2.legend(handles = [line,line2], title = "Update rate", loc = "upper right")


# g2.set_ylim(bottom = 0)
# g.set_ylim(bottom = 0, top = 50)

g.legend(loc = 'upper left', title = "Occurences")
# g2.legend(loc = 'upper right', title = "Update Rate")




g.set_xlabel("Number of encountered devices per hour")
g2.set_xlabel("Number of encountered devices per hour")
g2.set_ylabel("Update rate", fontsize = 15)
g.set_ylabel("Number of occurences", fontsize = 15)

axs.tick_params(axis='x', rotation=30)


plt.tight_layout(pad = 0.1)

fig.savefig("Rate_vs_Count_LinePlot_Histogram.png")

plt.clf()

######################################################################################

def get_remove(date):

  # print(date)

  if date.hour >= 6 and date.hour <= 23:
    return "No"
  else:
    return "Yes"

up_rates_int = pd.read_csv("Time_Interval_Rates.csv")

up_rates_int = up_rates_int.loc[up_rates_int['Time_Interval'] != "1 Min"]

up_rates_int['Date'] = up_rates_int['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

up_rates_int['Remove'] = up_rates_int['Date'].apply(lambda x: get_remove(x))


up_rates_int = up_rates_int.loc[up_rates_int['Remove'] != "Yes"]

# over_20 = up_rates_int.loc[(up_rates_int['Rate'] > 20) & (up_rates_int['Time_Interval'] == "1 Hour") & (up_rates_int['Device'] == 'Samsung')]
# print(over_20.head(10))

# up_rates_int = up_rates_int.rc[up_rates_int['Time_Interval']]

up_rates_int = up_rates_int.drop(up_rates_int[(up_rates_int.Time_Interval == '1 Hour') & ((up_rates_int.Rate < 4) | (up_rates_int.Rate > 20))].index)
# up_rates_int = up_rates_int.drop(up_rates_int[(up_rates_int.Time_Interval == '30 Min') & (up_rates_int.Rate == 0)].index)
# up_rates_int = up_rates_int.drop(up_rates_int[(up_rates_int.Time_Interval == '10 Min') & (up_rates_int.Rate == 0)].index)

fig, axs = plt.subplots(1, 1, figsize = (4.54, 3.54*1), dpi = 300)

g = sns.boxplot(data = up_rates_int, x = "Time_Interval", y = "Rate", hue = "Device", palette = palette_dict, showmeans = True, showfliers = False, meanprops={"markerfacecolor":"white", "markeredgecolor":"black"}, hue_order = ['Apple', 'Samsung'])

g.legend(loc = "upper right")
g.set_ylabel("Number of observed updates")
g.set_xlabel("Interval time")

plt.tight_layout(pad = 0.1)

plt.grid(color='#ABABAB', linewidth=0.1, zorder=0)

fig.savefig("Update_Rate_Intervals.png")

plt.clf()


####################################

# # plt.rc('xtick', labelsize=15) 
# plt.rc('xtick', labelsize=11)

# total = pd.read_csv("Rate_Count_Merged.csv")
# hist_data= pd.read_csv("Average_Count.csv")




# total['Hour'] = total['Hour'].apply(pd.to_numeric)
# total['Rate'] = total['Rate'].apply(pd.to_numeric)
# total = total.rename(columns = {"Count": "Device Count"})
# # total = total[['Device', 'Rate', 'Device Count']]
# total = total.sort_values(by = "Device Count")

# print(hist_data.head())
# print(total.head())


# fig, axs = plt.subplots(1, 1, figsize = (4.54*1, 3.54*1), dpi = 300, sharex = True)
# ax2 = axs.twinx()

# g = sns.barplot(data = hist_data, x = "Count", y = "Avg", hue = "Device", palette = palette_dict, hue_order = ['Apple', 'Samsung'], ax = axs, alpha = 0.3, order = ['1-10', '11-50', '> 50'])

# g2 = sns.boxplot(data = total, x = "Bucket", y = "Rate", hue = "Device", palette = palette_dict, hue_order = ['Apple', 'Samsung'], ax = ax2, showfliers = False, order = ['1-10', '11-50', '> 50'])


# print(len(g.patches))

# # hatches = ['//////' for i in range(44)]
# # hatches.extend('++++++' for i in range(44))

# # for i,thisbar in enumerate(g.patches):
# #     thisbar.set_hatch(hatches[i])



# g2.set_ylim(bottom = 0)
# g.set_ylim(bottom = 0, top = 200)

# g.legend().remove()
# g2.legend(loc = 'upper left')




# g.set_xlabel("Number of devices bucket")
# g2.set_xlabel("Number of devices bucket")
# g2.set_ylabel("Updates per hour", fontsize = 15)
# g.set_ylabel("Average number of devices", fontsize = 14)

# # axs.tick_params(axis='x', rotation=30)

# plt.tight_layout(pad = 0.1)

# fig.savefig("Rate_vs_Count_BoxPlots_Histogram.png")

# plt.clf()



#####################################################################################

# rates = pd.read_csv("10Min_Update_Rates.csv")

# rates['Rate'] = rates['Rate'].apply(lambda x: x*6)
# rates['Date'] = rates['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
# rates['Date'] = rates['Date'].apply(lambda x: x.strftime('%H:%M:%S'))

# print(rates['Date'].values[0])

# print(rates.head())

# x_ticks = ['18:00:00', '21:00:00', '06:00:00', '09:00:00', '12:00:00', '15:00:00']

# date_ticks = []

# # for i in x_ticks:
# #   datetime_object = datetime.strptime(i, '%H:%M:%S')
# #   date_ticks.append(datetime_object.strftime('%H:%M:%S'))

# # print(date_ticks)

# fig, axs = plt.subplots(1, 1, figsize = (3.54*4, 3.54*1), dpi = 300)

# g = sns.lineplot(data = rates, x = "Date", y = "Rate", hue = "Device", hue_order = ['Apple', 'Samsung', 'Combined'], palette = palette_colors, ax = axs)

# # g = sns.scatterplot(data = rates, x = "Date", y = "Rate", hue = "Device", hue_order = ['Apple', 'Samsung', 'Combined'], palette = palette_colors, ax = axs)

# g.set_ylabel("Update rate (pings/hour)")
# g.set_xlabel("Time of Day")

# g.set_xticklabels(date_ticks)
# plt.xticks(rotation = 30)

# plt.tight_layout(pad = 0.1)

# fig.savefig("10Min_Update_Rates.png")


#####################################################################################

# plt.rc('xtick', labelsize=8) 
# plt.rc('ytick', labelsize=10) 

# intervals = pd.read_csv("Update_Intervals.csv")

# # intervals = intervals.loc[intervals['Interval'] <= 100]

# fig, axs = plt.subplots(1, 1, figsize = (4.54*0.5, 3.54*0.75), dpi = 300)

# g = sns.boxplot(data = intervals, x = "Device", y = "Interval", order = ['Apple', 'Samsung', 'Combined'],palette = palette_colors, ax = axs, showmeans = True, showfliers = False, meanprops = {'markeredgecolor' : 'black'})

# g.set_ylabel("Time between\nupdates (min)", fontsize = 10)
# g.set_xlabel("")
# g.set_ylim((-2, 37))
# # plt.rc('xtick', labelsize=10) 
# # plt.rc('ytick', labelsize=15) 
# plt.xticks(rotation=30)

# plt.tight_layout(pad = 0.1)
# fig.savefig("Controlled_Intervals.png")



######################################################################################