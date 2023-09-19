import pandas as pd 
from haversine import haversine
from tqdm import tqdm

# def get_countries(user):

# 	return list(hex_to_country.loc[hex_to_country['ID'] == user]['Country'].unique())

# def get_country(row):

# 	return hex_to_country.loc[hex_to_country['h3_cell'] == row['h3_cell']]['Country']

def compare_list_of_coords(distance, device_coords, gps_coords):

	for d_coord in device_coords:

		for g_coord in gps_coords:

			if haversine(d_coord, g_coord) <= distance:
				# print("Haversine Match:", distance)
				return 1

	return -1


if __name__ == "__main__":

	distance = 0.5

	tqdm.pandas()

	times = [i*60 for i in range(1, 61)]

	total = pd.read_csv("./Data/No_HomeV3/Tag_Data_No_Home_Hexagons_Visited_Countries.csv")
	total = total.sort_values(by = "Adjusted_Time", ascending = True, ignore_index = True)

	# hex_to_country = pd.read_csv("./Data/No_HomeV3/Hexagon_To_Countries.csv")

	# total['Country'] = total.progress_apply(lambda row: get_country(row), axis = 1)

	# total.to_csv("./Data/No_HomeV3/Tag_Data_No_Home_Hexagons_Visited_Countries.csv")

	user_dataframes = {}

	percentages = {}

	users = list(total['ID'].unique())

	for user in users:

		sliced = total.loc[total['ID'] == user]

		percentages[user] = {}

		user_countries = list(sliced['Country'].unique())
		for country in user_countries:
			percentages[user][country] = {}

		user_dataframes[user] = {}
		user_dataframes[user]['DataFrame'] =  sliced
		user_dataframes[user]['Countries'] = user_countries

	

	# for time in times:
	# 	percentages[time] = {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}}


	#from 1 to 60
	for time_interval in times:

		for user in tqdm(users):

			for country in user_dataframes[user]['Countries']:

				num_buckets = 0

				percentages[user][country][time_interval] = {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}}

				df = user_dataframes[user]['DataFrame']

				df_c = df.loc[df['Country'] == country]

				max_time = df_c.tail(1)['Adjusted_Time'].values[0]

				for i, row in df_c.iterrows():

					if row['Source'] == 'GPS':

						first_timestamp = row['Adjusted_Time']

						break


				while True:

					bucket = df_c.loc[(df_c['Adjusted_Time'] >= first_timestamp) & (df_c['Adjusted_Time'] <= first_timestamp + time_interval)]

					gps_df = bucket.loc[bucket['Source'] == 'GPS']
					apple_df = bucket.loc[bucket['Source'] == 'Apple']
					samsung_df = bucket.loc[bucket['Source'] == 'Samsung']


					if len(gps_df) > 0:
						
						num_buckets += 1

					
					if len(apple_df) > 0 or len(samsung_df) > 0:

						gps_df = gps_df[['Latitude', 'Longitude']]
						gps_coords = list(gps_df.itertuples(index = False, name = None))


						percentages[user][country][time_interval]['Combined']['found'] = False

						if len(apple_df) > 0:
							
							apple_df = apple_df[['Latitude', 'Longitude']]
							apple_coords = list(apple_df.itertuples(index = False, name = None))

							result = compare_list_of_coords(distance, apple_coords, gps_coords)

							if result == 1:
								percentages[user][country][time_interval]['Apple']['count'] += 1
								
								if percentages[user][country][time_interval]['Combined']['found'] == False:
									percentages[user][country][time_interval]['Combined']['found'] = True
									percentages[user][country][time_interval]['Combined']['count'] += 1


						if len(samsung_df) > 0:
							
							samsung_df = samsung_df[['Latitude', 'Longitude']]
							samsung_coords = list(samsung_df.itertuples(index = False, name = None))

							result = compare_list_of_coords(distance, samsung_coords, gps_coords)

							if result == 1:

								percentages[user][country][time_interval]['Samsung']['count'] += 1

								if percentages[user][country][time_interval]['Combined']['found'] == False:
									percentages[user][country][time_interval]['Combined']['found'] = True
									percentages[user][country][time_interval]['Combined']['count'] += 1




					first_timestamp = first_timestamp + time_interval
					if first_timestamp >= max_time:
						break

				for device in percentages[user][country][time_interval]:
					percentages[user][country][time_interval][device]['Per'] = float(percentages[user][country][time_interval][device]['count']/num_buckets)


	times = []
	device = []
	p = []
	us = []
	cs = []

	output = pd.DataFrame(columns = ['User', 'Country', 'Device', 'Time', 'Percentage'])

	for user in percentages:

		for country in percentages[user]:

			for t in percentages[user][country]:

				for d in percentages[user][country][t]:

					cs.append(country)
					us.append(user)
					times.append(t)
					device.append(d)
					p.append(percentages[user][country][t][d]['Per'])


	output['User'] = us
	output['Country'] = cs
	output['Device'] = device
	output['Time'] = times
	output['Percentage'] = p


	output.to_csv("./Data/No_HomeV3/500m_Time_Sweep_Probability_Visited5Min.csv")












