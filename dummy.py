import math

# Define the coordinates of the two points
point1 = (-12824, 69, -10873)
point2 = (-12814, 69, -10887)

# Calculate the distance using the Euclidean distance formula
distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)

print(f"The distance between point1 and point2 is {distance}")