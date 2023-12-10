import numpy as np

def encode_points(points):

    assert len(points.shape) == 2, "Points must be a 2D array"

    def average_dist(points):
        distances = []
        for i in range(len(points)):
            for j in range(i+1, len(points)):
                distances.append(np.linalg.norm(points[i] - points[j]))
        return np.mean(distances)

    def sort_by_coordinates(points):
        
        return np.array(sorted(points, key=lambda x: (x[0], x[1])))

    def translate_to_origin(points):
        centroid = np.mean(points, axis=0)
        return points - centroid

    avg_distance = np.round(average_dist(points), 4)
    points_translated = translate_to_origin(points)
    points_sorted = np.round(sort_by_coordinates(points_translated), 4)
    
    # Convert to string format

    points_str = ",".join([f"{x},{y}" for x, y in points_sorted])
    encoding = f"{points_str}:{{{avg_distance}}}"

    return encoding

import numpy as np

def decode(encoded_str):
    # Split the string by the colon to separate points and average distance
    point_strs, avg_distance_str = encoded_str.split(":")
    
    # Convert average distance back to float
    # avg_distance = float(avg_distance_str)
    
    # Split the point strings by the comma and convert back to float
    points = np.array([list(map(float, point_str.split(','))) for point_str in point_strs.split(":")])
    
    return points

# Function to fetch and decode data from the database
def fetch_and_decode(db_path = '10Conf.db', table_name = 'configurations'):
    import sqlite3
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute SQL query to fetch all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # print(rows)
    
    # Decode each row and print it
    decoded_rows = []
    for row in rows:
        _, encoded_str, energy = row
        points = decode(encoded_str)
        decoded_rows.append((points, energy))
        # print(f"Points: {points}, Energy: {energy}")
    
    # Close the connection
    conn.close()
    
    return decoded_rows
