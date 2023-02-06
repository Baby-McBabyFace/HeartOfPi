def a2cTranslate(obs_data): #android to client translation
    obs_data = obs_data.replace("(", "").replace(")", "").split(",")
    x = 10 * int(obs_data[0]) + 5
    y = 200 - (10 * int(obs_data[1])) - 5
    return [x, y, int(obs_data[3]), int(obs_data[0]) + 1]