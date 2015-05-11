def pretty_print(list, entries_per_line=4):
    #prints out agents to console in a non-barbaric fashion, does not return outuput
    liNums = range(len(list))
    x = 0
    line = ""
    for i in liNums:
        x += 1
        line += str(list[i]) + "    "
        if not x % entries_per_line:
            line += "\n"
    # send line to output, here I will just print it
    print line
    
def get_key(item):
    """A very complex function.
    
    Args:
        item: an item
        
    Returns:
        item[1]: the second value in item
    """

    #helper function for run_generation
    return item[1] 
