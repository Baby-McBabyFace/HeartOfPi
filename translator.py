def android2clientTranslate(obs_data): #android to client translation
    obs_list = []
    for data in obs_data:
        data = data.replace("(", "").replace(")", "").split(",")
        x = 10 * int(data[1]) + 5
        y = 200 - (10 * int(data[2])) - 5
        obs_list.append([x, y, int(data[3]), int(data[0]) + 1])
    return obs_list

def client2stmTranslate(movement): #client to stm translation
    move = movement[0]
    displacement = movement[1:]
    
    if(move == 'w'): # forward movement
        return 1, 0, int(displacement)

    elif(move == 's'): # reverse movement
        return 2, 0, int(displacement)
    
    elif(move == 'q'): # left movement
        return 3, int(displacement), None
    
    elif(move == 'e'): # right movement
        return 4, int(displacement), None
    
    elif(move == 'a'): # reverse left movement
        return 5, int(displacement), None
    
    elif(move == 'd'): # reverse right movement
        return 6, int(displacement), None
    
    elif(move == 'p'): # take picture
        return 7, int(displacement), None
    
    else:
        return None, None, None