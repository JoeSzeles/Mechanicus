import os
from config import*

def get_blocks(gcode_lines):
    block_counter = 0
    blocks = []
    current_block = []
    first_block = True
    
    for line in gcode_lines:
        if line.startswith('G0') or line.startswith('G1'):
            block_counter += 1
            current_block.append(line.strip())
            
            # Check if the current block is complete
            if block_counter == 6:
                # Add the current block to the list of blocks
                blocks.append(current_block)
                
                # Reset the block counter and current block
                block_counter = 0
                current_block = []
                
        else:
            # Check if the current block is complete and add it to the list of blocks
            if current_block and (len(current_block) == 6 or (first_block and len(current_block) < 6)):
                blocks.append(current_block)
                
                # Check if this is the first block and if it is complete
                if first_block and len(current_block) == 6:
                    # Set line 3 to Z0 for first block
                    current_block[2] = current_block[2].replace('Z' + str(zDraw), 'Z0')
                    
            # Reset the block counter and current block
            block_counter = 0
            current_block = []
            
            # Check if this is the first block
            if first_block:
                first_block = False
            else:
                # Add a separator line between blocks
                blocks.append(['; block separator'])
            
    # Check if the last block is complete and add it to the list of blocks
    if current_block and len(current_block) == 6:
        blocks.append(current_block)
    
    return blocks





def correct_gcode_file(file_path):
    # read contents of file into list of strings
    with open(file_path, 'r') as file:
        gcode_lines = file.readlines()

    # get list of blocks from gcode file
    blocks = get_blocks(gcode_lines)

    # modify blocks to set Z coordinate to 0
    for block in blocks:
        block[0] = block[0].replace('Z5.000', str(zLift))
        if len(block) >= 2:
            block[1] = block[1].replace('Z5.000', str(zLift))

    # get path and filename for corrected gcode file
    save_path = os.path.splitext(file_path)[0] + '_corrected.gcode'

    # write modified blocks to new gcode file
    with open(save_path, 'w') as file:
        for block in blocks:
            for line in block:
                file.write(line + '\n')

    print('Gcode file corrected and saved as', save_path)

correct_gcode_file('switch18.gcode')