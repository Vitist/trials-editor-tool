import sys
import os
import shutil

# Get the track folder path from parameters
trackPath = sys.argv[1]

# Editor track folders always end with this
folderEnd = "-0-0000000000000"

# Track and metadata file headers
metadataHeader = ['da', '7a', 'ba', 'be', '0f']
# Redlynx plz
trackHeaderUplay = ['de', 'ad', 'ba', 'be', '09', '00', '00', '00', '2c']
trackHeaderSteam = ['ca', 'fe', 'b0', '0b', '09', '00', '00', '00', '2c']

# User identifiers
vitist = ['4b', 'f0', '01', '61', 'bc', '05', '97', '67', '6a',
          '50', 'b5', '32', '2a', '15', '9c', 'd5']

drollest = ['4b', 'f0', '01', '61', 'bc', '05', '97', '67', '6a',
            '50', 'b5', '32', '2a', '15', '9c', 'd5']

haarmes = ['4b', 'f0', '01', '61', 'bc', '05', '97', '67', '6a',
           '50', 'b5', '32', '2a', '15', '9c', 'd5']

kaketsu = ['44', '2a', '6e', '04', '80', 'e1', '3b', 'c9', '8d',
           '1b', '63', 'dd', '25', '87', '8b', 'b6']

# Select user
user = vitist
trackHeader = trackHeaderUplay

# Get every folder from path
pathFolders = trackPath.split("\\")
# Split into track folder and parent folder
trackFolder = pathFolders[-1]
parentFolder = pathFolders[:-1]
# Get the unique user and track identifier part
trackAndUserID = trackFolder.split("-")[0]
# Get the unique track identifier part
trackId = trackAndUserID[32:]
# Create a folder name with different user identifier
newTrackFolder = "".join(user) + trackId + folderEnd
# Create full path for the new track folder
parentFolder.append(newTrackFolder)
parentFolder[0] = parentFolder[0] + "\\"
newTrackPath = os.path.join(*parentFolder)

# Create the new folder and copy files from the old folder
print("Copying files from: " + trackPath + "\nto: " + newTrackPath)
shutil.copytree(trackPath, newTrackPath)

# Read track file contents
print("\nModifying file: " + newTrackPath + "\\track.trk")
with open(newTrackPath + "\\track.trk", "rb") as trackFile:
    trackFileHex = ["{:02x}".format(c) for c in trackFile.read()]

# Change track file header
newTrackFileHex = trackHeader + user + trackFileHex[25:]

# Write changes to track file
with open(newTrackPath + "\\track.trk", "wb") as trackFile:
    newTrackFileBytes = bytearray.fromhex("".join(newTrackFileHex))
    for i in newTrackFileBytes:
        trackFile.write(bytes((i,)))

# Read metadata file contents
print("Modifying file: " + newTrackPath + "\\metadata.mda")
with open(newTrackPath + "\\metadata.mda", "rb") as metadataFile:
    metadataFileHex = ["{:02x}".format(c) for c in metadataFile.read()]

# Change metadata file header
newMetadataFileHex = metadataHeader + user + metadataFileHex[21:]

# Write changes to metadata file
with open(newTrackPath + "\\metadata.mda", "wb") as metadataFile:
    newMetadataFileBytes = bytearray.fromhex("".join(newMetadataFileHex))
    for i in newMetadataFileBytes:
        metadataFile.write(bytes((i,)))

# Wait before exit
# os.system("pause")
