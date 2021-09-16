#
# This is not actually run by d2gifcompile.py, but it was used to create units_pylist.txt
# Takes a Photoshop .act file and returns a list of hex values for each color
# 
# # Source: https://stackoverflow.com/a/48873783

from codecs import encode

def act_to_list(act_file):
    with open(act_file, 'rb') as act:
        raw_data = act.read()                           # Read binary data
    hex_data = encode(raw_data, 'hex')                  # Convert it to hexadecimal values
    total_colors_count = (int(hex_data[-7:-4], 16))     # Get last 3 digits to get number of colors total
    misterious_count = (int(hex_data[-4:-3], 16))       # I have no idea what does it do
    colors_count = (int(hex_data[-3:], 16))             # Get last 3 digits to get number of nontransparent colors

    print(total_colors_count)

    # Decode colors from hex to string and split it by 6 (because colors are #1c1c1c)               
    colors = [hex_data[i:i+6].decode() for i in range(0, total_colors_count*6, 6)]

    # Add # to each item and filter empty items if there is a corrupted total_colors_count bit        
    colors = ['#'+i for i in colors if len(i)]

    return colors