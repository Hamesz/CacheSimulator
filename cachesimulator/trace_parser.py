def parse(file):
    """Parses the text file 

    Args:
        file ([type]): [description]
    """
    lines = read_text(file)
    lines = modify_lines(lines)
    return lines

def modify_lines(lines):
    """Modifies the lines so:
        [cache.id, command as a method, address]

    Args:
        lines (list(string)): each line in the text
    """
    parsed_lines = []
    for line in lines:
        words = line.split(' ')

        if (len(words) == 3):
            # expect a proper command to be given
            uid = int(words[0][1])    # get the last char of p1
            method = words[1]
            address = int(words[2])
            line = [uid, method, address]    
        else:
            if (words[0] != 'p' and words[0] != 'h' and words[0] != 'v'):
                raise Exception('Unknown trace file input {}, expected (p, v, h)'.format(words[0]))
            line = [-1, words[0], -1]
        parsed_lines.append(line)
    return parsed_lines

def read_text(file_path):
    """Reads the file into a list

    Args:
        file (string): path to the file to read
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f]
    return lines