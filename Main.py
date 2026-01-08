import csv
import re

with open('stats_22_05_16_13_22_10.csv', newline='') as csvfile:
     reader = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
     data = [row for row in reader]


def stringToFloat(data):
    '''Takes a string
       Return float after ":"
    '''
    try:
        data = data.split(":", 1)[1]
        num = re.search((r'\d+(\.\d*)?'), data).group()
        return float(num)
        
    except Exception:
        return 0


def data_name(string):
    '''Takes a string
       Return substring before ":"
    '''
    if (string.find(":") >= 0):
        string = string.split(":", 1)[0]
    return (string)


def display_delta(line1, line2): #void
    '''Takes 2 int
       Prints deltas (line2 - line1)
    '''
    for i in range(len(data[line1])):
        cell1 = data[line1][i]
        cell2 = data[line2][i]
      
        if(not cell1 or not cell2):
           print(str(i+1) + ": "+"Empty cell(s)")
           continue
          
        cell1_analyse = stringToFloat(cell1)
        cell2_analyse = stringToFloat(cell2)
        res = cell2_analyse - cell1_analyse

        if(res>0):
           print("\x1b[1;30;47m" +str(i+1) + ": " + str(data_name(cell1)) +": +"+ str(res) + "\x1b[0m")
        elif(res<0):
           print("\x1b[1;30;41m" + str(i+1) + ": " + str(data_name(cell1)) +": "+ str(res) + "\x1b[0m")
        else:
           print("\x1b[0;37;40m" + str(i+1) + ": " + str(data_name(cell1)) +": "+ str(res) + "\x1b[0m")


def display_line(line):
    '''Takes int
       Prints line's datas
    '''
    for i in range (len(data[line])):
       if(data[line][i]):
         print(str(i+1) + ": " + data[line][i])
       else:
          print("EMPTY")  


def direction(dir):
    '''Takes a string
       Return an int (lines to add)
    '''
    if(dir=='n' or dir=='p'):
      return 1
    if(dir.find(' ')>=0):
       dir = dir.split(' ', 1)[0]

    add = re.search((r'\d+(\.\d*)?'), dir).group()
    return int(add)
       

def delta(dir):
    '''Takes a string
       Return an int (delta's line)
    '''
    if(dir.find(' ')>=0):
       dir = dir.split(' ', 1)[1]
    
    delt_line =int(re.search((r'\d+(\.\d*)?'), dir).group())
    if(delt_line<=0 or delt_line>(len(data))):
        return 0
    return delt_line-1



print("\n --- SUMMARY (Last to first line delta) --- \n")
display_delta(0, -1)

line = 0
delt_line=0
while(line>=0 and line<=(len(data)-1)): 

    print("\n --- Line " + str(line+1) + ": --- \n")
    display_line(line)
    
    print("\n --- Line " + str(line+1) + " (delta line " + str(delt_line+1) + "): --- \n")
    display_delta(delt_line, line)
      
    dir = input("\nCONTROLS:\nnext (n) previous (p) delta (d):") 
    char_dir = list(dir)
    
    for i in range(len(char_dir)):
       if (char_dir[i]=="n"):
         line += direction(dir)
       elif (char_dir[i]=="p"):
         line -= direction(dir)

       if (char_dir[i]=="d"):
         delt_line = delta(dir)
       else: #default
         delt_line = line-1


print("\x1b[4;31;40m" + "Error message" + "\x1b[0m")



