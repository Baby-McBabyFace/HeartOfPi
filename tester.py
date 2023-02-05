
myList = [["f030"], ["r090"], ["f050"]]

for i in myList:
    print(i[0])
    if(i[0][:1] == "f"):
        move = 1
        i[0] = i[0][:1]
    elif(i[0] == "r"):
        move = 4

print(myList)