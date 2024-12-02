# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		https://discord.com/chan- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from enum import Enum, auto
import itertools


class GameAction(Enum):
    OPEN = auto()
    FLAG = auto()


class Variable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.constraints = set()

    def add_constraint(self, x, y):
        self.constraints.add((x, y))
        if len(self.constraints) > 8:
            raise Exception('A variable cannot be associated to more than 8 constraints')

class Constraint:
    def __init__(self, x, y, sum):
        if not 0 <= sum < 9:
            raise ValueError('Adjacent mine count (%d) must be in [0, 9)' % sum)

        self.x = x
        self.y = y
        self.sum = sum
        self.variables = set()

    def add_variable(self, x, y):
        self.variables.add((x, y))
        if len(self.variables) > 8:
            raise Exception('A constraint cannot have more than 8 variables')

class MinesweeperCSP:
    def __init__(self, rowDimension, colDimension, totalMines, board):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.board = board
        self.constraints = {}
        self.variables = {}
        self.safe_cells = set()
        self.mine_cells = set()

    def create_constraint_graph(self):
        self.constraints = {}
        self.variables = {}
        for x in range(self.rowDimension):
            for y in range(self.colDimension):
                if isinstance(self.board[x][y], int) and self.board[x][y] > 0:
                    self.register_constraint(x, y)

    def register_constraint(self, x, y):
        flagged_mines, constraint_variables = self.find_constraint_variables(x, y)
        if constraint_variables:
            adjacent_mine_count = self.board[x][y]
            constraint_value = adjacent_mine_count - len(flagged_mines)
            new_constraint = Constraint(x, y, constraint_value)
            self.constraints[(x, y)] = new_constraint
            for variable_position in constraint_variables:
                variable = self.variables.setdefault(variable_position, Variable(*variable_position))
                variable.add_constraint(x, y)
                new_constraint.add_variable(*variable_position)

    def neighbours(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i == j == 0) and 0 <= x + i < self.rowDimension and 0 <= y + j < self.colDimension:
                    yield (x + i, y + j)

    def find_constraint_variables(self, x, y):
        hidden_neighbours = {neighbour for neighbour in self.neighbours(x, y)
                             if self.board[neighbour[0]][neighbour[1]] == '?'}
        flagged_neighbours = {neighbour for neighbour in hidden_neighbours
                              if neighbour in self.mine_cells}
        unflagged_neighbours = hidden_neighbours - flagged_neighbours
        return flagged_neighbours, unflagged_neighbours

    def solve_trivial_constraints(self):
        solved_constraints = []
        for constraint in self.constraints.values():
            if constraint.sum == 0:
                for variable in constraint.variables:
                    solved_constraints.append((GameAction.OPEN, variable))
            elif constraint.sum == len(constraint.variables):
                for variable in constraint.variables:
                    solved_constraints.append((GameAction.FLAG, variable))
        return solved_constraints

    def apply_actions(self, actions):
        for action in actions:
            type, (x, y) = action
            if type == GameAction.OPEN:
                self.safe_cells.add((x, y))
            else:
                self.mine_cells.add((x, y))
    def apply_bomb_rule(self):
        for x in range(self.rowDimension):
            for y in range(self.colDimension):
                # Check if the current cell is a numbered cell
                if isinstance(self.board[x][y], int) and self.board[x][y] > 0:
					# Find neighbors
                    neighbors = list(self.neighbors(x, y))
                    hidden_neighbors = [neighbor for neighbor in neighbors if self.board[neighbor[0]][neighbor[1]] == '?']
                    
                    # Count unflagged bombs around it
                    flagged_mines = [neighbor for neighbor in hidden_neighbors if neighbor in self.mine_cells]
                    unflagged_bombs_remaining = self.board[x][y] - len(flagged_mines)
					
					# If the number of hidden neighbors equals the number of unflagged bombs remaining
                    if len(hidden_neighbors) == unflagged_bombs_remaining:
						# All hidden neighbors must be flagged as bombs
                        for(nx, ny) in hidden_neighbors:
                            self.mine_cells.add((nx, ny))  # Mark the cell as a mine
                            self.safe_cells.discard((nx, ny))  # Remove from safe cells
                            self.board[nx][ny] = 'M'  # Update the board to reflect that it's a mine
                            print(f"Bomb rule applied: Flagging ({nx}, {ny}) as a mine.")
                            
    def apply_no_bomb_rule(self):                        
        for x in range(self.rowDimension):
            for y in range(self.colDimension):
                # Check if the current tile is a numbered tile (greater than 0)
                if isinstance(self.board[x][y], int) and self.board[x][y] > 0:
                    # Find neighbors
                    neighbors = list(self.neighbours(x, y))
                    hidden_neighbors = [neighbor for neighbor in neighbors if self.board[neighbor[0]][neighbor[1]] == '?']
                    
                    # Count the number of flagged bombs around the tile
                    flagged_mines = [neighbor for neighbor in hidden_neighbors if neighbor in self.mine_cells]
                    flagged_count = len(flagged_mines)
                    
                    # Get the number on the current tile
                    tile_value = self.board[x][y]
                    
                    # Check if the number of flagged bombs equals the number on the tile
                    if flagged_count == tile_value:
                        # All remaining hidden neighbors must be safe (not bombs)
                        for (nx, ny) in hidden_neighbors:
                            # Mark the cell as safe (i.e., not a bomb)
                            self.safe_cells.add((nx, ny))  # Add it to safe cells
                            self.mine_cells.discard((nx, ny))  # Remove from mine cells
                            self.board[nx][ny] = 'S'  # Update the board to reflect that it's safe
                            print(f"No bomb rule applied: Marking ({nx}, {ny}) as safe.")


class MyAI(AI):  # Line 164
    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):  # Line 165
        self.board = [['?' for _ in range(colDimension)] for _ in range(rowDimension)]
        self.safe_cells = set()
        self.mine_cells = set()
        self.frontier = []  # List to store frontier cells
        self.uncovered = set()  # Set to store uncovered cells
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.to_explore = [(startX, startY)]
        self.board[startX][startY] = 0
        self.csp = MinesweeperCSP(rowDimension, colDimension, totalMines, self.board)
        self.csp.create_constraint_graph()
        print(f"Line 178: Initialized board with starting point ({startX}, {startY})")  # Line 178

    def get_neighbors(self, row, col):  # Line 180
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.rowDimension and 0 <= new_col < self.colDimension:
                    neighbors.append((new_row, new_col))
        print(f"Line 189: Neighbors of ({row}, {col}): {neighbors}")  # Line 189
        return neighbors

    def apply_constraints(self):
        print("Line 193: Applying constraints")  # Line 193

        # Use CSP to solve trivial constraints or apply any CSP-specific logic
        solved_constraints = self.csp.solve_trivial_constraints()
        # Apply those constraints (actions can be OPEN or FLAG)
        for action in solved_constraints:
            self.apply_actions([action])

        # Other CSP-related actions, like applying the bomb rule or no-bomb rule
        self.csp.apply_bomb_rule()
        self.csp.apply_no_bomb_rule()

        # Now handle cell exploration logic (this part is separate from CSP)
        for row in range(self.rowDimension):
            for col in range(self.colDimension):
                if isinstance(self.board[row][col], int) and self.board[row][col] > 0:
                    neighbors = self.get_neighbors(row, col)
                    flagged_count = sum(1 for (r, c) in neighbors if self.board[r][c] == 'M')
                    hidden_neighbors = [(r, c) for (r, c) in neighbors if self.board[r][c] == '?']
                    num_mines_needed = self.board[row][col] - flagged_count

                    print(f"Line 214: Cell ({row}, {col}) with value {self.board[row][col]} has {flagged_count} flagged mines and needs {num_mines_needed} more mines. Hidden neighbors: {hidden_neighbors}")  # Line 212

                    if num_mines_needed == len(hidden_neighbors):
                        for (r, c) in hidden_neighbors:
                            self.enforce_binary_domain(r, c, True)
                    elif num_mines_needed == 0:
                        for (r, c) in hidden_neighbors:
                            self.enforce_binary_domain(r, c, False)

    def reveal_safe_cells(self):  # Line 221
        print("Line 224: Revealing safe cells")  # Line 224
        while self.safe_cells:
            row, col = self.safe_cells.pop()
            if self.board[row][col] == '?':
                self.to_explore.append((row, col))
                self.board[row][col] = 'S'
                self.uncovered.add((row, col))  # Add to uncovered set
                print(f"Line 231: Revealed safe cell at ({row, col})")  # Line 231

    def mark_mines(self):  # Line 233
        print("Line 234: Marking mines")  # Line 234
        for (row, col) in self.mine_cells:
            if self.board[row][col] == '?':
                self.board[row][col] = 'M'
                self.uncovered.add((row, col))  # Add to uncovered set
                print(f"Line 239: Marked mine at ({row, col})")  # Line 239

    def getAction(self, number: int) -> Action:  # Line 241
        print(f"Line 242: Getting action with number {number}")  # Line 242
        self.apply_constraints()
        self.reveal_safe_cells()
        self.mark_mines()

		# Process cells to explore
        while self.to_explore:
            row, col = self.to_explore.pop(0)
            if (row, col) not in self.uncovered:
                print(f"Line 251: Uncovering cell at ({row}, {col})")  # Line 251
                self.uncovered.add((row, col))  # Mark as uncovered
				# Add neighboring cells to the exploration queue
                neighbors = self.get_neighbors(row, col)
                for (r, c) in neighbors:
                    if self.board[r][c] == '?' and (r, c) not in self.uncovered:
                        self.to_explore.append((r, c))
                    return Action(AI.Action.UNCOVER, row, col)

		# Flag cells identified as mines
        if self.mine_cells:
            row, col = self.mine_cells.pop()
            if (row, col) not in self.uncovered:
                print(f"Line 264: Flagging mine at ({row}, {col})")  # Line 264
                self.uncovered.add((row, col))  # Mark as uncovered
                return Action(AI.Action.FLAG, row, col)
        print("Line 267: No more actions possible, leaving the game")  # Line 267
        return Action(AI.Action.LEAVE)
