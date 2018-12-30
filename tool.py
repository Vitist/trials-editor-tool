import sys
import os
import shutil

# Get the track folder path from parameters
trackPath = sys.argv[1]
programPath = os.path.dirname(sys.argv[0])
# Editor track folders always end with this
folderEnd = "-0-0000000000000"

# Track and metadata file headers
metadataHeader = ['da', '7a', 'ba', 'be', '0f']
# Redlynx plz
trackHeaderUplay = ['de', 'ad', 'ba', 'be', '09', '00', '00', '00', '2c']
trackHeaderSteam = ['ca', 'fe', 'b0', '0b', '09', '00', '00', '00', '2c']

try:
    # Read "key=value" style config file
    with open(programPath + "\\config.txt", "r") as configFile:
        userId = configFile.readline().split("=")[1]
        platform = configFile.readline().split("=")[1]
except FileNotFoundError:
    # No config file found, create it
    with open(programPath + "\\config.txt", "w+") as configFile:
        print("No config file found, running initial setup.")
        # Get user identifier from track folder name
        userId = input("\nCreate a new track in the editor and copy its folder name\n"
                       "from C:\\Users\\*USERNAME*\\Documents\\TrialsFusion\\SavedGames here:\n")
        userId = userId[:32]

        # Get users platform
        platform = ''
        while platform not in ('u', 's'):
            platform = input("Which platform did you purchase the game from? Steam(s), Uplay(u): ")

        # Save users info to config file
        config = ["id=" + userId, "platform=" + platform]
        configFile.write('\n'.join(config))

# Select user
user = [userId[i:i+2] for i in range(0, len(userId), 2)]
if platform == 'u':
    trackHeader = trackHeaderUplay
else:
    trackHeader = trackHeaderSteam

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
try:
    print("Copying files from: " + trackPath + "\nto: " + newTrackPath)
    shutil.copytree(trackPath, newTrackPath)
except FileExistsError:
    print("\nThis track has already been modified to work in the editor.")
else:
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
