import sys
trackFolder = sys.argv[1]

vitist = ['de', 'ad', 'ba', 'be', '09', '00', '00', '00', '2c', '4b', 'f0', '01', '61', 'bc', '05', '97', '67', '6a',
          '50', 'b5', '32', '2a', '15', '9c', 'd5']

print("Opening folder: " + trackFolder)
with open(trackFolder + "\\track.trk", "rb") as trackFile:
    trackFileHex = ["{:02x}".format(c) for c in trackFile.read()]

newTrackFileHex = vitist + trackFileHex[25:]

with open(trackFolder + "\\track.trk", "wb") as f:
    newTrackFileBytes = bytearray.fromhex("".join(newTrackFileHex))
    for i in newTrackFileBytes:
        f.write(bytes((i,)))
