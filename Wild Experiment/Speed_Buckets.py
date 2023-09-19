
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


def get_speed(df):

	first_point = df.head(1)
	last_point = df.tail(1)

	first_point_lat = float(first_point['Latitude'])
	first_point_lon = float(first_point['Longitude'])
	last_point_lat = float(last_point['Latitude'])
	last_point_lon = float(last_point['Longitude'])

	distance = haversine((first_point_lat,first_point_lon), (last_point_lat, last_point_lon))


	speed = distance*12

	if speed <= 0.2:
		return 'Stationary'
	elif speed <= 6.0:
		return 'Pedestrian'
	elif speed <= 12.0:
		return 'Jogging'
	else:
		return 'Transit'



def compare_list_of_coords(distance, device_coords, gps_coords):

	for d_coord in device_coords:

		for g_coord in gps_coords:

			if haversine(d_coord, g_coord) <= distance:
				return 1

	return -1


if __name__ == "__main__":

	total = pd.read_csv("./Data/No_HomeV3/Tag_Data_No_Home_Hexagons_Visited_Countries.csv")
	total = total.sort_values(by = "Adjusted_Time", ascending = True, ignore_index = True)

	time_interval = 300

	distances = [0.01, 0.1, 0.5, 1.0, 5.0]

	speeds = ['Stationary', 'Pedestrian', 'Jogging', 'Transit']

	user_dataframes = {}

	users = list(total['ID'].unique())

	for user in users:

		sliced = total.loc[total['ID'] == user]

		if user == 'Yasir':
			sliced = sliced.loc[sliced['Country'] != 'UAE']

		user_dataframes[user] = {}
		user_dataframes[user]['DataFrame'] =  sliced
		user_dataframes[user]['MaxTime'] = int(sliced.tail(1)['Adjusted_Time'])


	#speed, distance, device/num_buckets, count

	percentages = {}

	for speed in speeds:
		percentages[speed] = {0.01: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 0.1: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 0.5: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 1.0: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}, 5.0: {'Apple': {'count': 0}, 'Samsung': {'count': 0}, 'Combined': {'count': 0, 'found' : False}, 'num_buckets': 0}}	


	for user in users:

		if user == 'Thomas':
			continue
		
		df = user_dataframes[user]['DataFrame']
		for i, row in df.iterrows():
			if row['Source'] == 'GPS':
				first_timestamp = row['Adjusted_Time']
				break

		while True:

			bucket = df.loc[(df['Adjusted_Time'] >= first_timestamp) & (df['Adjusted_Time'] <= first_timestamp + time_interval)]

			gps_df = bucket.loc[bucket['Source'] == 'GPS']
			apple_df = bucket.loc[bucket['Source'] == 'Apple']
			samsung_df = bucket.loc[bucket['Source'] == 'Samsung']

			if len(gps_df) > 0:

				speed = get_speed(gps_df)

				print(speed)

				for distance in distances:
					percentages[speed][distance]['num_buckets'] += 1

				if len(apple_df) > 0 or len(samsung_df) > 0:

					gps_df = gps_df[['Latitude', 'Longitude']]
					gps_coords = list(gps_df.itertuples(index = False, name = None))

					for distance in distances:

						percentages[speed][distance]['Combined']['found'] = False

						if len(apple_df) > 0:
							
							apple_df = apple_df[['Latitude', 'Longitude']]
							apple_coords = list(apple_df.itertuples(index = False, name = None))

							result = compare_list_of_coords(distance, apple_coords, gps_coords)

							if result == 1:
								percentages[speed][distance]['Apple']['count'] += 1
								
								if percentages[speed][distance]['Combined']['found'] == False:
									percentages[speed][distance]['Combined']['found'] = True
									percentages[speed][distance]['Combined']['count'] += 1


						if len(samsung_df) > 0:
							
							samsung_df = samsung_df[['Latitude', 'Longitude']]
							samsung_coords = list(samsung_df.itertuples(index = False, name = None))

							result = compare_list_of_coords(distance, samsung_coords, gps_coords)

							if result == 1:

								percentages[speed][distance]['Samsung']['count'] += 1

								if percentages[speed][distance]['Combined']['found'] == False:
									percentages[speed][distance]['Combined']['found'] = True
									percentages[speed][distance]['Combined']['count'] += 1




			first_timestamp = first_timestamp + time_interval

			if first_timestamp >= user_dataframes[user]['MaxTime']:
				break


	print(percentages)


	out_file = open("./Data/No_HomeV3/Speed_Bucket_Percentages_No_Yasir_UAE.json", "w")
	json.dump(percentages, out_file, indent = 6)
	out_file.close()


	speeds = []
	devices = []
	distances = []
	pers = []

	output = pd.DataFrame(columns = ['Speed', 'Radius', 'Device', 'Percentage'])

	for speed in percentages:
		for distance in percentages[speed]:
			for device in percentages[speed][distance]:

				if device != "num_buckets":
					speeds.append(speed)
					devices.append(device)
					distances.append(distance)

					pers.append(percentages[speed][distance][device]['count']/percentages[speed][distance]['num_buckets'])

	output['Device'] = devices
	output['Radius'] = distances
	output['Percentage'] = pers
	output['Speed'] = speeds

	output.to_csv("./Data/No_HomeV3/Speed_Bucket_Percentages_No_Yasir_UAE.csv")












