from copy import deepcopy

class EnvOps():

    #wrapper to deal with frameskip
    def nfs_step(env, move):
        observation, reward, terminated, trunc, info = env.step(move)
        for i in range(3):
            env.step(move)
        return observation, reward, terminated, trunc, info

    def get_pixels(coords):
        x, y = coords
        coords_to_pixels = {
            'x': [20, 37, 54, 70, 85, 100, 117, 133],
            'y': [180, 160, 140, 120, 95, 70, 50, 30]
        }   
        return coords_to_pixels['x'][x-1], coords_to_pixels['y'][y-1]

    def get_empty_squares(board):
        empty_squares = []
        for x in range(1,9):
            for y in range(1,9):
                x_px, y_px = EnvOps.get_pixels((x,y))
                if board[y_px][x_px] == 104:
                    empty_squares.append((x,y))
        return empty_squares

    #square validity check using env.step()
    # def check_square_validity(env, curr_coord, check_coord) -> bool: #, board, player
    #     temp_env = deepcopy(env)
    #     reward = 0
    #     moves = EnvOps.get_moves_to_position(curr_coord, check_coord)
    #     for move in moves:
    #         EnvOps.nfs_step(temp_env, move)
    #     observation, reward, terminated, trunc, info = EnvOps.nfs_step(temp_env, 1)
    #     if reward != 0:
    #         return True
    #     return False

    #square validity check using manual check of game state
    def check_square_validity(curr_coord, board, player) -> bool:
        #get coords for 8 adjacent squares
        adj_squares = []
        for i in range(2,10):
            adj_coord, wraparound = EnvOps.move_one((curr_coord[0],curr_coord[1]), i)
            if not wraparound:  #only include touching squares
                adj_squares.append(adj_coord)

        #check adjacent squares for opponent's discs
        adj_opponent_squares = []
        for coord in adj_squares:
            x, y = coord[0], coord[1]
            x_px, y_px = EnvOps.get_pixels(coord)
            
            if board[y_px][x_px] == 0 and player == 1:
                adj_opponent_squares.append(coord)
            elif board[y_px][x_px] == 212 and player == -1:
                adj_opponent_squares.append(coord)
        
        if not adj_opponent_squares: return False

        #check if adjacent opponent discs are flanked by friendly discs
        for coord in adj_opponent_squares:
            #traverse axis in direction of opponent disc
            x_step, y_step = coord[0]-curr_coord[0], coord[1]-curr_coord[1]
            coord = list(coord)
            while 0 not in coord and 9 not in coord:    #traverse one direction across axis until edge of board
                x_px, y_px = EnvOps.get_pixels(coord)
                match board[y_px][x_px]:
                    case 212:   #white disc
                        if player == 1: return True
                        else:
                            coord[0] += x_step
                            coord[1] += y_step
                    case 0:    #black disc
                        if player == -1: return True
                        else:
                            coord[0] += x_step
                            coord[1] += y_step
                    case 104:   #empty square, check next adjacent opponent square/axis
                        break
        return False
    
    #returns coords resulting from moving one position
    def move_one(start, move):
        wraparound = False
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
        if y < 1 or y > 8 or x<1 or x>8:
            wraparound = True
            if y < 1: y += 8
            elif y > 8: y -= 8
            if x < 1: x += 8
            elif x > 8: x -= 8

        return (x, y), wraparound

    #returns tuple of moves that take the environment from the start coords to the destination coords
    def get_moves_to_position(start, destination):
        moves = []
        x_diff = start[0]-destination[0]
        y_diff = start[1]-destination[1]
        if x_diff < 0:
            for i in range(-1*x_diff): moves.append(3)
        elif x_diff > 0:
            for i in range(x_diff): moves.append(4)
        if y_diff < 0:
            for i in range(-1*y_diff): moves.append(2)
        elif y_diff > 0:
            for i in range(y_diff): moves.append(5)

        # while (x, y) != destination:
        #     x_diff = x-destination[0]
        #     y_diff = y-destination[1]
        #     move = -1
        #     if x_diff < 0 and y_diff < 0:
        #         move = 6
        #     elif x_diff < 0 and y_diff == 0:
        #         move = 3
        #     elif x_diff < 0 and y_diff > 0:
        #         move = 8
        #     elif x_diff > 0 and y_diff < 0:
        #         move = 7
        #     elif x_diff > 0 and y_diff == 0:
        #         move = 4
        #     elif x_diff > 0 and y_diff > 0:
        #         move = 9
        #     elif x_diff == 0 and y_diff < 0:
        #         move = 2
        #     elif x_diff == 0 and y_diff > 0:
        #         move = 5
            
        #     x, y = EnvOps.move_one((x,y), move)
        #     moves.append(move)
        return tuple(moves)