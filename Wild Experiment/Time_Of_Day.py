
#split dataframe into individual users
#for each user, get a 5 minute bucket
#for each bucket, calculate the average speed,
#for each bucket, get a list of gps coordinates, apple coordinates, and samsung coordinates
#check each apple and samsung location against all gps coordinates, if we find a hit, then we increment and break
#move to next bucket
#each bucket increments 1 to count
#each hit increments 1 to specific area in dictionary

import pandas as pd 
from haversine import haversine
import json
from tzwhere import tzwhere
from datetime import datetime, timedelta
import warnings


def visited(hexagon, user):

	if len(visited_hexagons.loc[(visited_hexagons['h3'] == hexagon) & (visited_hexagons['ID'] == user)]) > 0:
		return True
	else:
		return False


def get_time(latitude, longitude, time):

	location = tz.tzNameAt(latitude, longitude)

	try:

		zone = str(time_zones.loc[time_zones['TZ_Name'] == location]['DST'].values[0])

		if "−" == zone[0]:

			zone_int = int(zone[1:zone.index(":")])
			zone_int = zone_int * -1

		else:
			zone_int = int(zone[1:zone.index(":")])

		date_time = datetime.fromtimestamp(time)

		adjusted_date_time = date_time + timedelta(zone_int)

		hour = adjusted_date_time.hour

		# return hour
		if hour >= 6 and hour <10:
			return 'Morning'
		elif hour >=10 and hour < 14:
			return 'Lunch'
		elif hour >= 14 and hour < 18:
			return 'Afternoon'
		elif hour >= 18 and hour < 22:
			return 'Evening'
		else:
			return 'Night'

	except:
		print(location)
		return 'Unknown'

def compare_list_of_coords(distance, device_coords, gps_coords):

	for d_coord in device_coords:

		for g_coord in gps_coords:

			if haversine(d_coord, g_coord) <= distance:
				return 1

	return -1


if __name__ == "__main__":

	warnings.filterwarnings("ignore")
	tz = tzwhere.tzwhere()
	time_zones = pd.read_csv("./Data/Time_Zone_Conversion.csv")
	total = pd.read_csv("./Data/No_HomeV3/Tag_Data_No_Home_Hexagons_Visited_Countries.csv")
	total = total.sort_values(by = "Adjusted_Time", ascending = True, ignore_index = True)

	time_interval = 300

	distances = [0.01, 0.1, 0.5, 1.0, 5.0]

	times = ['Morning', 'Lunch', 'Afternoon', 'Evening', 'Night']

	user_dataframes = {}

	users = list(total['ID'].unique())

	for user in users:

		sliced = total.loc[total['ID'] == user]

		if user == "Yasir":

			sliced = sliced.loc[sliced['Country'] != 'UAE']

		user_dataframes[user] = {}
		user_dataframes[user]['DataFrame'] =  sliced
		user_dataframes[user]['MaxTime'] = int(sliced.tail(1)['Adjusted_Time'])


	#speed, distance, device/num_buckets, count

	percentages = {}

	for time in times:
		percentages[time] = {}

	for user in users:

		df = user_dataframes[user]['DataFrame']

		user_hexagons = list(df['h3_cell'].unique())

		count = 0

		for i, hexagon in enumerate(user_hexagons):

			count += 1

			# if visited(hexagon, user) == False:
			# 	continue

			entries_in_hexagon = df.loc[df['h3_cell'] == hexagon]
			entries_in_hexagon = entries_in_hexagon.sort_values(by = "Adjusted_Time")
			max_time = int(entries_in_hexagon.tail(1)['Adjusted_Time'])



			for i, row in df.iterrows():
				if row['Source'] == 'GPS':
					first_timestamp = row['Adjusted_Time']
					break

			while True:

				bucket = entries_in_hexagon.loc[(entries_in_hexagon['Adjusted_Time'] >= first_timestamp) & (entries_in_hexagon['Adjusted_Time'] <= first_timestamp + time_interval)]

				gps_df = bucket.loc[bucket['Source'] == 'GPS']
				apple_df = bucket.loc[bucket['Source'] == 'Apple']
				samsung_df = bucket.loc[bucket['Source'] == 'Samsung']

				if len(gps_df) > 0:

					time = get_time(gps_df.head(1)['Latitude'], gps_df.head(1)['Longitude'], gps_df.head(1)['Adjusted_Time'])

					print(time)

					if time == 'Unknown':
						first_timestamp = first_timestamp + time_interval
						continue

					if hexagon not in percentages[time]:
						percentages[time][hexagon] = {0.01: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 0.1: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 0.5: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 1.0: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 5.0: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}}	

					
					for distance in distances:
						percentages[time][hexagon][distance]['num_buckets'] += 1

					if len(apple_df) > 0 or len(samsung_df) > 0:

						gps_df = gps_df[['Latitude', 'Longitude']]
						gps_coords = list(gps_df.itertuples(index = False, name = None))

						for distance in distances:

							percentages[time][hexagon][distance]['Combined']['found'] = False

							if len(apple_df) > 0:
								
								apple_df = apple_df[['Latitude', 'Longitude']]
								apple_coords = list(apple_df.itertuples(index = False, name = None))

								result = compare_list_of_coords(distance, apple_coords, gps_coords)

								if result == 1:
									percentages[time][hexagon][distance]['Apple']['count'] += 1
									
									if percentages[time][hexagon][distance]['Combined']['found'] == False:
										percentages[time][hexagon][distance]['Combined']['found'] = True
										percentages[time][hexagon][distance]['Combined']['count'] += 1


							if len(samsung_df) > 0:
								
								samsung_df = samsung_df[['Latitude', 'Longitude']]
								samsung_coords = list(samsung_df.itertuples(index = False, name = None))

								result = compare_list_of_coords(distance, samsung_coords, gps_coords)

								if result == 1:

									percentages[time][hexagon][distance]['Samsung']['count'] += 1

									if percentages[time][hexagon][distance]['Combined']['found'] == False:
										percentages[time][hexagon][distance]['Combined']['found'] = True
										percentages[time][hexagon][distance]['Combined']['count'] += 1




				first_timestamp = first_timestamp + time_interval

				if first_timestamp >= user_dataframes[user]['MaxTime']:
					break


	print(percentages)


	out_file = open("./Data/No_HomeV3/Time_Bucket_Hexagon_Percentages_Visited_No_YASIR_UAE.json", "w")
	json.dump(percentages, out_file, indent = 6)
	out_file.close()


	times = []
	devices = []
	distances = []
	pers = []
	hexagons = []
	numBuckets = []

	output = pd.DataFrame(columns = ['Time', 'Hexagon', 'Buckets', 'Radius', 'Device', 'Percentage'])

	for time in percentages:
		for hexagon in percentages[time]:
			for distance in percentages[time][hexagon]:
				for device in percentages[time][hexagon][distance]:
					if device != "num_buckets" and percentages[time][hexagon][distance]['num_buckets'] != 0:
						times.append(time)
						devices.append(device)
						distances.append(distance)
						hexagons.append(hexagon)
						numBuckets.append(percentages[time][hexagon][distance]['num_buckets'])
						pers.append(percentages[time][hexagon][distance][device]['count']/percentages[time][hexagon][distance]['num_buckets'])

	
	output['Hexagon'] = hexagons
	output['Buckets'] = numBuckets
	output['Device'] = devices
	output['Radius'] = distances
	output['Percentage'] = pers
	output['Time'] = times

	output.to_csv("./Data/No_HomeV3/Time_Hexagon_Bucket_Percentages_Visited_5MinResolution_No_YASIR_UAE.csv")












