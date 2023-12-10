import pandas as pd

#problem 1
def generate_car_matrix():
    # Read the dataset-1.csv file into a DataFrame
    df = pd.read_csv('dataset-1.csv')

    # Create a matrix using set_index, unstack, and fillna
    matrix = df.set_index(['id_1', 'id_2'])['car'].unstack(fill_value=0) 

    # Set diagonal values to 0 using a loop
    for i in range(len(matrix)):
        matrix.iloc[i, i] = 0
        
    return matrix

# Example usage
result_matrix = generate_car_matrix()
print(result_matrix)


# problem 2
def get_type_count(df):
    # Add a new categorical column 'car_type' based on conditions
    df['car_type'] = df['car'].apply(lambda x: 'low' if x <= 15 else ('medium' if x <= 25 else 'high'))

    # Calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))

    return sorted_type_counts

# Example usage
df = pd.read_csv('dataset-1.csv')
result_type_counts = get_type_count(df)
print(result_type_counts)



#problem 3
def get_bus_indexes(df):
    # Calculate the sum and count of 'bus' values
    bus_sum = df['bus'].sum()
    bus_count = len(df['bus'])

    # Calculate the mean value of 'bus' manually
    mean_bus = bus_sum / bus_count
    
    print(mean_bus)

    # Identify the indices where 'bus' values are greater than twice the mean value
    bus_indexes = [index for index in range(len(df['bus'])) if df['bus'][index] > 2 * mean_bus]

    return bus_indexes

# Example usage
df = pd.read_csv('dataset-1.csv')
result_indexes = get_bus_indexes(df)
print(result_indexes)

#problem 4
def filter_routes(df):
    # Calculate the sum and count of 'truck' values
    truck_sum = df['truck'].sum()
    truck_count = len(df['truck'])
    
    # Calculate the average of 'truck' manually
    truck_avg = truck_sum / truck_count 
    
    filtered_data = truck_avg+7
    print(truck_avg)
    
    for each_df in df:
        
        #filtered_routes = [each_df['route'] for each_df in df if int(each_df['truck']) > filtered_data]
        filtered_routes = [row['truck'] for _, row in df.iterrows() if int(row['truck']) > filtered_data]

   
        filtered_routes.sort()
        return filtered_routes
    
     

df = pd.read_csv('dataset-1.csv')
result_indexes = filter_routes(df)
print(result_indexes)

#problem 5
def multiply_matrix(matrix):
    # Create a copy of the matrix to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Apply the specified logic to modify values in the DataFrame
    for i in range(len(modified_matrix)):
        for j in range(len(modified_matrix.columns)):
            if modified_matrix.iloc[i, j] > 20:
                modified_matrix.iloc[i, j] *= 0.75
            else:
                modified_matrix.iloc[i, j] *= 1.25

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

# Example usage
result_matrix = generate_car_matrix()  # Assuming you have the result from Question 1
modified_matrix = multiply_matrix(result_matrix)
print(modified_matrix)

#problem 6

from datetime import datetime, timedelta

def verify_timestamps(df):
    incorrect_pairs = []

    for (id, id_2), group in df.groupby(['id', 'id_2']):
        start_timestamp = datetime.strptime(str(group['startDay'].iloc[0]) + ' ' + str(group['startTime'].iloc[0]), '%A %H:%M:%S')
        end_timestamp = datetime.strptime(str(group['endDay'].iloc[0]) + ' ' + str(group['endTime'].iloc[0]), '%A %H:%M:%S')
        duration = end_timestamp - start_timestamp

        if duration < timedelta(hours=24) or len(group) < 7:
            incorrect_pairs.append((id, id_2))
           
    return pd.Series(data=True, index=pd.MultiIndex.from_tuples(incorrect_pairs, names=['id', 'id_2']))

df = pd.read_csv('dataset-2.csv')
incorrect_timestamps = verify_timestamps(df)
print(incorrect_timestamps)
