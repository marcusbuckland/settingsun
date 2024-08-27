import numpy as np

N_ROWS = 5
N_COLS = 4
VALID_COORDS = {(r, c) for r in range(N_ROWS) for c in range(N_COLS)}
WIN_COORDS = {(r, c) for r in range(3, 5) for c in range(1, 3)}
DIRECTIONS = ["LEFT", "RIGHT", "UP", "DOWN"]

class SettingSun:
    def __init__(self):
        self.board = np.zeros(shape=(N_ROWS, N_COLS))
        self.solution = None

    def setup(self):
        pieces = [1, 0, 0, 2, 1, 0, 0, 2, -1, 3, 3, -1, 4, 6, 7, 5, 4, 8, 9, 5]
        coords = [(r, c) for r in range(N_ROWS) for c in range(N_COLS)]

        for p, c in zip(pieces, coords):
            self.board[c] = p

    def solve_setting_sun(self):
        positions = set()
        positions.add(self.get_position())
        solution = []
        
        if self.solve(positions=positions, solution=solution):
            self.show_solution()
        else:
            print("No solution found!")

    def solve(self, positions, solution):
        # base case
        if self.has_finished() : 
            self.solution = solution
            return True

        pos = self.get_position()
        if pos in positions : return False # No progress- I've been here before!!

        # recursive case
        valid_moves = self.get_valid_moves()
        for p, d in valid_moves.items():
            self.move_piece(p, d)
            new_pos = self.get_position()
            positions.add(new_pos)
            solution.append(f"Move piece {p}: {d}")

            if self.solve(positions=positions, solution=solution):
                return True
            
            # backtrack
            solution.pop()
            positions.remove(new_pos)

        return False

    def get_empty_cells(self):
        """Returns coordinates of empty cells in board"""
        return self.get_piece_coords(-1)
    
    def get_sun(self):
        """Returns coordinates of the "sun" piece"""
        return set(self.get_piece_coords(0))
    
    def get_position(self):
        return str([self.get_piece_coords(p)[0] for p in range(10)])

    def get_piece_coords(self, piece):
        return [(r, c) for r, c in np.argwhere(self.board == piece)]
    
    def get_updated_piece_coords(self, piece, direction):
        match direction:
            case "LEFT":
                return {(r, c-1) for r, c in self.get_piece_coords(piece)}
            case "RIGHT":
                return {(r, c+1) for r, c in self.get_piece_coords(piece)}
            case "UP":
                return {(r-1, c) for r, c in self.get_piece_coords(piece)}
            case "DOWN":
                return {(r+1, c) for r, c in self.get_piece_coords(piece)}

    def update_board(self, piece, coords):
        """Updates the board, placing the piece specified to the coords specified.
        Called during "move" methods."""
        for r, c in coords:
            self.board[r, c] = piece

    def move_piece(self, piece, direction):
        match direction:
            case "LEFT" : self.move_piece_left(piece)
            case "RIGHT" : self.move_piece_right(piece)
            case "UP" : self.move_piece_up(piece)
            case "DOWN" : self.move_piece_down(piece)

    def move_piece_left(self, piece):
        coords = self.get_updated_piece_coords(piece, "LEFT")
        self.board[np.where(self.board==piece)] = -1 # remove piece
        self.update_board(piece, coords)

    def move_piece_right(self, piece):
        coords = self.get_updated_piece_coords(piece, "RIGHT")
        self.board[np.where(self.board==piece)] = -1 # remove piece
        self.update_board(piece, coords)

    def move_piece_up(self, piece):
        coords = self.get_updated_piece_coords(piece, "UP")
        self.board[np.where(self.board==piece)] = -1 # remove piece
        self.update_board(piece, coords)

    def move_piece_down(self, piece):
        coords = self.get_updated_piece_coords(piece, "DOWN")
        self.board[np.where(self.board==piece)] = -1 # remove piece
        self.update_board(piece, coords)

    def is_valid_move(self, piece, direction):
        coords = self.get_updated_piece_coords(piece, direction)
        rows = {c[0] for c in coords}
        cols = {c[1] for c in coords}
        
        # Check that all coordinates are in-bounds.
        if not coords.issubset(VALID_COORDS) : return False

        # Check that there is space for the piece to move into.
        match direction:
            case "LEFT":
                l = {(r, min(cols)) for r in rows} # Coordinates to check if trying to move left.
                return {-1} == set([self.board[c] for c in l])
            case "RIGHT":
                r = {(r, max(cols)) for r in rows} # Coordinates to check if trying to move right.
                return {-1} == set([self.board[c] for c in r])
            case "UP":
                u = {(min(rows), c) for c in cols} # Coordinates to check if trying to move up
                return {-1} == set([self.board[c] for c in u])
            case "DOWN":
                d = {(max(rows), c) for c in cols} # Coordinates to check if trying to move down.
                return {-1} == set([self.board[c] for c in d])

        # Shouldn't be possible to make it here.
        raise Exception()

    def get_valid_moves(self):
        moves = {k:[] for k in range(10)}

        for piece in moves:
            for direction in DIRECTIONS:
                if self.is_valid_move(piece=piece, direction=direction):
                    moves[piece].append(direction)

        return moves

    def has_finished(self):
        return self.get_sun() == WIN_COORDS
    
    def show_solution(self):
        for step in self.solution:
            print(step)

if __name__ == '__main__':
    s = SettingSun()
    s.setup()
    s.solve_setting_sun()
