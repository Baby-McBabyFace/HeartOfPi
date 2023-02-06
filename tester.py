
myCommand = "START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"

mylist = []
command = myCommand.split('/')
instruction = command.pop(0)


if(instruction == "START"):
    task = command.pop(0)
    
    if(task == "EXPLORE"):
        robot_pos = command.pop(0).replace("(", "").replace(")", "").split(",")
        for obs_data in command:
            obs_data = obs_data.replace("(", "").replace(")", "").split(",")
            x = 10 * int(obs_data[0]) + 5
            y = 200 - (10 * int(obs_data[1])) - 5
            mylist.append([x, y, int(obs_data[3]), int(obs_data[0])])
    elif(task == "PATH"):
        print(2)

print(mylist)

# for i in myList:
#     print(i[0])
#     if(i[0][:1] == "f"):
#         move = 1
#         i[0] = str(move) + i[0][1:]
#     elif(i[0] == "r"):
#         move = 4

# print(myList)