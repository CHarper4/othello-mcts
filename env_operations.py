
class EnvOps():

    #wrapper to deal with frameskip
    def nfs_step(env, move):
        observation, reward, terminated, trunc, info = env.step(move)
        env.step(move)
        env.step(move)
        env.step(move)
        return observation, reward, terminated, trunc, info

    coords_to_pixels = {
        'x': [20, 37, 54, 70, 85, 100, 117, 133],
        'y': [180, 160, 140, 120, 95, 70, 50, 30]
    }

    def get_empty_squares(board):
        empty_squares = []
        for x in range(1,9):
            for y in range(1,9):
                x_px, y_px = EnvOps.coords_to_pixels['x'][x-1], EnvOps.coords_to_pixels['y'][y-1]
                if board[y_px][x_px] == 104:
                    empty_squares.append((x,y))
        return empty_squares

    def check_square_validity(check_coord, board) -> bool:
        adj_coords = []
        for i in range(2,10):
            adj_coords.append(EnvOps.move_one((check_coord[0],check_coord[1]), i))

        #check adjacent squares for black discs
        adj_black_squares = []
        for coord in adj_coords:
            x, y = coord[0], coord[1]
            x_px, y_px = EnvOps.coords_to_pixels['x'][x-1], EnvOps.coords_to_pixels['y'][y-1]
            if board[y_px][x_px] == 0:
                adj_black_squares.append(coord)
        if not adj_black_squares: return False

        #check if adjacent black discs are flanked by white discs
        for coord in adj_black_squares:
            coord = list(coord)
            #traverse axis in direction of black disc
            x_step, y_step = coord[0]-check_coord[0], coord[1]-check_coord[1]
            while 0 not in coord and 9 not in coord:
                x_px, y_px = EnvOps.coords_to_pixels['x'][coord[0]-1], EnvOps.coords_to_pixels['y'][coord[1]-1]
                match board[y_px][x_px]:
                    case 212:   #white disc, square is valid
                        print("white disc")
                        return True
                    case 104:   #empty square, check next adjacent black square
                        print("empty square")
                        break
                    case 0:    #black disc, check next square along axis
                        print("black disc")
                        coord[0] += x_step
                        coord[1] += y_step
        return False #reached end of board
    
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
        if y < 1: y += 8
        elif y > 8: y -= 8
        if x < 1: x += 8
        elif x > 8: x -= 8

        return x, y

    #returns tuple of moves that take the environment from the start coords to the destination coords
    def get_moves_to_position(start, destination):
        moves = []
        x, y = start
        x_diff = x-destination[0]
        y_diff = y-destination[1]
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