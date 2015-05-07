

def pretty_print(list,entriesPerLine=4):
    #prints out agents to console in a non-barbaric fashion, does not return outuput
    liNums = range(len(list))
    x = 0
    line = ""
    for i in liNums:
        x+=1
        line += str(list[i]) +"    "
        if not x%entriesPerLine:
            line += "\n"
    #send line to output, here I will just print it
    print line
    
def getKey(item):
    #helper function for run_generation
    return item[1] 