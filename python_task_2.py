import pandas as pd

#problem 1
def calculate_distance_matrix(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file, sep=None, engine='python', header=0, names=['id_start', 'id_end', 'distance'])

    # Print column names for debugging
    print("Column names:", df.columns)

    # Initialize an empty dictionary to store cumulative distances
    distances = {}

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Initialize variables before iterating through columns
        id_start, id_end, distance = None, None, None

        # Iterate through columns (id_start, id_end, distance) in the row
        for col, value in row.items():
            # Extract ID_start, ID_end, and distance from the row
            if col == 'id_start':
                id_start = value
            elif col == 'id_end':
                id_end = value
            elif col == 'distance':
                distance = value

        # Add the distance to the cumulative distance between ID_start and ID_end
        if id_start is not None and id_end is not None and distance is not None:
            if (id_start, id_end) in distances:
                distances[(id_start, id_end)] += distance
            else:
                distances[(id_start, id_end)] = distance

            # Ensure the matrix is symmetric by adding the distance in the reverse direction
            distances[(id_end, id_start)] = distances[(id_start, id_end)]

    # Create a DataFrame from the distances dictionary
    distance_matrix = pd.DataFrame(index=df['id_start'].unique(), columns=df['id_start'].unique())

    # Fill the DataFrame with cumulative distances
    for (id_start, id_end), distance in distances.items():
       distance_matrix.at[id_start, id_end] = distance

  

    # Fill diagonal values with 0
    distance_matrix.fillna(0, inplace=True)

    return distance_matrix

# Example usage
csv_file = 'dataset-3.csv'
result_matrix = calculate_distance_matrix(csv_file)
print(result_matrix)

#problem 2
def unroll_distance_matrix(distance_matrix):
    # Initialize an empty list to store unrolled distance data
    unrolled_data = []

    # Iterate through rows and columns of the distance_matrix
    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            # Skip if id_start is equal to id_end
            if id_start == id_end:
                continue
            
            # Extract distance from the distance_matrix
            distance = distance_matrix.at[id_start, id_end]

            # Append the data to the unrolled_data list
            unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    # Create a DataFrame from the unrolled_data list
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

# Example usage 
unrolled_result = unroll_distance_matrix(result_matrix)
print("\nQuestion 2 Result:")
print(unrolled_result.to_string())

#problem 3
def find_ids_within_ten_percentage_threshold(df, reference_value):
    # Filter rows with the given reference_value in the id_start column
    reference_rows = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference_value
    average_distance = reference_rows['distance'].mean()

    # Calculate the threshold range (10% of the average_distance)
    threshold_range = 0.1 * average_distance

    # Find IDs within the threshold range
    ids_within_threshold = df[(df['distance'] >= average_distance - threshold_range) &
                               (df['distance'] <= average_distance + threshold_range)]['id_start'].unique()

    # Sort the list of IDs
    ids_within_threshold = sorted(ids_within_threshold)

    return ids_within_threshold

# Example usage 
reference_value = 1001402  # Replace with the desired reference_value
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_result, reference_value)
print("IDs within 10% threshold of average distance for reference value {}: {}".format(reference_value, result_within_threshold))

#problem 4
def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Initialize columns for each vehicle type in the DataFrame
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate_coefficient

    return df

# Example usage 
toll_rate_result = calculate_toll_rate(unrolled_result)
print("\nQuestion 4 Result:")
print(toll_rate_result.to_string())

#problem 5
import datetime

def calculate_time_based_toll_rates(df):
    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(datetime.time(0, 0, 0), datetime.time(10, 0, 0)),
                           (datetime.time(10, 0, 0), datetime.time(18, 0, 0)),
                           (datetime.time(18, 0, 0), datetime.time(23, 59, 59))]
    
    weekend_time_range = (datetime.time(0, 0, 0), datetime.time(23, 59, 59))

    # Add columns for start_day, start_time, end_day, and end_time
    df['start_day'] = df['start_time'] = df['end_day'] = df['end_time'] = None

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Extract start and end times
        start_time_str = row['start_time']
        end_time_str = row['end_time']

        # Check for None values
        if start_time_str is None or end_time_str is None:
            continue

        start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M:%S').time()

        # Set start_day and end_day
        df.at[index, 'start_day'] = df.at[index, 'end_day'] = start_time.strftime('%A')

        # Set start_time and end_time based on the time ranges
        if start_time < weekday_time_ranges[0][0]:
            df.at[index, 'start_time'] = weekday_time_ranges[0][0]
        elif start_time < weekday_time_ranges[1][0]:
            df.at[index, 'start_time'] = weekday_time_ranges[1][0]
        else:
            df.at[index, 'start_time'] = weekday_time_ranges[2][0]

        if end_time < weekday_time_ranges[0][0]:
            df.at[index, 'end_time'] = weekday_time_ranges[0][0]
        elif end_time < weekday_time_ranges[1][0]:
            df.at[index, 'end_time'] = weekday_time_ranges[1][0]
        else:
            df.at[index, 'end_time'] = weekday_time_ranges[2][0]

        # Apply discount factors based on time ranges
        if start_time < weekday_time_ranges[0][1]:
            df.at[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8
        elif start_time < weekday_time_ranges[1][1]:
            df.at[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= 1.2
        else:
            df.at[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.8

        # If it's a weekend, apply a constant discount factor of 0.7
        if start_time >= weekend_time_range[0] and end_time <= weekend_time_range[1]:
            df.at[index, ['moto', 'car', 'rv', 'bus', 'truck']] *= 0.7

    return df

# Example usage for Question 5
time_based_toll_rates_result = calculate_time_based_toll_rates(unrolled_result)
print(time_based_toll_rates_result.to_string())
