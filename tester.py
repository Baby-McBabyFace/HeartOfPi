import translator
import str2list

input01 = "START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"
print(f"Input01 (ANDROID SEND TO PI): {input01}\t{type(input01)}\n")
input01 = input01.split('/')
instruction = input01.pop(0)

if(instruction == "START"):
    task = input01.pop(0)
    
    if(task == "EXPLORE"): # EXAMPLE: "START/EXPLORE/(R,04,03,0)/(00,08,10,90)/(01,12,06,-90)"
        robot_pos = input01.pop(0).replace("(", "").replace(")", "").split(",")
        output01 = translator.android2clientTranslate(obs_data=input01)

print(f"Output01 (PI SEND TO PC WITH ALGO): {output01}\t{type(output01)}\n")

input02 = "[['w030'], ['e090'], ['w050'], ['d000'], ['p001']]"
print(f"Input02 (PC WITH ALGO SEND TO PI): {input02}\t{type(input02)}\n")

print(f"Output02 (PI SEND TO STM):")
path = input02
path = str2list.convert(path)
for movement in path:
    move, val1, val2 = translator.client2stmTranslate(movement[0])
    if(move == 7):
        # TAKE PICTURE
        print("TAKE PIC")
    elif(val2 is None):
        print("STM_ANGLE: dir:{}, angle:{}".format(move, val1))
    else:
        print("STM_AXIS: dir:{}, x:{}, y:{}".format(move, val1, val2))
        
