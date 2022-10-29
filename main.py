#Import statements
import pandas as pd

#Reading csv file
cData = pd.read_csv("celestial_data.csv")

#Removing incomplete rows
for col in cData.columns:
    cData = cData[cData[col].notna()]

#Converting mass, radius and disc_date rows to float-point values
cData[['mass', 'radius', 'discovery_date']] = cData[['mass', 'radius', 'discovery_date']].apply(pd.to_numeric)

#Converting mass and radius to solar mass and solar radius, respectively
cData['mass'] = cData['mass'] * 0.000954588
cData['radius'] = cData['radius'] * 0.102763

#Saving to new file
cData.to_csv('cleaned_celestial_data.csv', index=False)

#Reading from new file (important, because the indexes of the previous cData was haphazard due to the deletion process)
cData = pd.read_csv("cleaned_celestial_data.csv")
#Reading the other file
sData = pd.read_csv("stellar_data.csv")

#Cleaning up not-required columns
s_cols = ['v_mag', 'bayer_designation', 'spectral_class', 'luminosity']
for cols in s_cols:
    del sData[cols]

c_cols = ['constellation', 'right_ascension', 'declination', 'apparent_magnitude', 'spectral_type', 'discovery_date']
for cols in c_cols:
    del cData[cols]

#Creating headers for merged data
merged_headers = ['name', 'distance', 'mass', 'radius']

#Merging Data
#Index: 0 = name; 1 = distance; 2 = mass; 3 = radius;
data = []
for col in sData:
    row_data = []
    for row in sData[col]:
        row_data.append(row)
    data.append(row_data)

#Included i as a flag variable to make sure the proper data gets appended in the proper place
#Also had to append directly to data variable because appending row_data would introduce another nested list
i = 0
for col in cData:
    for row in cData[col]:
        data[i].append(row)
    i += 1

#Data seperation for simplicity
name = data[0]
distance = data[1]
mass = data[2]
radius = data[3]

#Creating a merged dataframe using the zip() method
zipped_data = list(zip(name, distance, mass, radius))
merged_data = pd.DataFrame(zipped_data,columns=merged_headers)

#Saving to csv file
merged_data.to_csv('merged_data.csv', index=False)