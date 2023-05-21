#print progressbar
def print_progress_bar(*args): #total lines, current line
    total_lines = int(args[0])
    current_line = int(args[1])
    fill = '█'
    printEnd = "\r"
    length = 50
    percent = float(current_line/total_lines*100)
    filledLength = int(length * current_line // total_lines)
    bar = fill * filledLength + '-' * (length - filledLength)
    return bar
