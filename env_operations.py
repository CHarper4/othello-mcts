
class EnvOps():

    #wrapper to deal with frameskip
    def nfs_step(env, move):
        observation, reward, terminated, trunc, info = env.step(move)
        env.step(move)
        env.step(move)
        env.step(move)
        return observation, reward, terminated, trunc, info
    
    #returns coords resulting from moving one position
    def move_one(start, move):
        x, y = start[0], start[1]
        match move:
            case 2:
                y += 1
            case 3:
                x += 1
            case 4:
                x -= 1
            case 5:
                y -= 1
            case 6:
                x += 1
                y += 1
            case 7:
                x -= 1
                y += 1
            case 8:
                x += 1
                y -= 1
            case 9:
                x -= 1
                y -= 1

        #wraparound
        if y <= 0: y += 8
        elif y > 8: y -= 8
        if x <= 0: x += 8
        elif x > 8: x -= 8

        return x, y

    #returns tuple of moves that take the environment from the start coords to the destination coords
    def get_moves_to_position(start, destination):
        moves = []
        x, y = start
        while (x, y) != destination:
            x_diff = x-destination[0]
            y_diff = y-destination[1]
            move = -1
            if x_diff < 0 and y_diff < 0:
                move = 6
            elif x_diff < 0 and y_diff == 0:
                move = 3
            elif x_diff < 0 and y_diff > 0:
                move = 8
            elif x_diff > 0 and y_diff < 0:
                move = 7
            elif x_diff > 0 and y_diff == 0:
                move = 4
            elif x_diff > 0 and y_diff > 0:
                move = 9
            elif x_diff == 0 and y_diff < 0:
                move = 2
            elif x_diff == 0 and y_diff > 0:
                move = 5
            
            x, y = EnvOps.move_one((x,y), move)
            moves.append(move)
        return tuple(moves)