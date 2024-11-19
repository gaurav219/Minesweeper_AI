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


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        def backtracking_search(csp):
            return backtrack(csp, {})


        def backtrack(csp, assignment):
            if is_complete(assignment, csp):
                return assignment
    
            var = select_unassigned_variable(csp, assignment)

            for value in csp.domains[var]:

                if is_consistent(var, value, assignment, csp):
                    assignment[var] = value
                    result = backtrack(csp, assignment)
                if result is not None:
                    return result
                del assignment[var]
            return None

        def is_complete(assignment, csp):
            if len(assignment) == len(csp.variables):
                return True
            else 
                return False

        def select_unassigned_variable(csp, assignment):
            for var in csp.variables:
                if var not in assignment:
                    return var

        def is_consistent(var, value, assignment, csp):
            for constraint in csp.constraints[var]:
                if not constraint.is_satisfied(assignment):
                    return False
            return True
	
	def get_neighbors(self, row, col):
        """Get all valid neighbors of a cell at (row, col) on the board."""
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue  # Skip the cell itself
                new_row, new_col = row + i, col + j
                if 0 <= new_row < self.rowDimension and 0 <= new_col < self.colDimension:
                    neighbors.append((new_row, new_col))
        return neighbors

	def apply_constraints(self):
		"""
		Applies the Neighbor Sum Constraint and handles Boundary Constraints.
		Updates self.safe_cells and self.mine_cells accordingly.
		"""
		for row in range(self.rowDimension):
			for col in range(self.colDimension):
				# Only consider revealed cells with numbers
				if isinstance(self.board[row][col], int) and self.board[row][col] > 0:
					neighbors = self.get_neighbors(row, col)
					
					# Count the number of flagged mines among the neighbors
					flagged_count = sum(1 for (r, c) in neighbors if self.board[r][c] == 'M')
					
					# Count the number of hidden cells among the neighbors
					hidden_cells = [(r, c) for (r, c) in neighbors if self.board[r][c] == '?']
					
					# Apply the Neighbor Sum Constraint
					num_mines_needed = self.board[row][col] - flagged_count
					
					# If the number of needed mines matches the number of hidden neighbors,
					# all hidden neighbors must be mines
					if num_mines_needed == len(hidden_cells):
						self.mine_cells.update(hidden_cells)
					
					# If no more mines are needed, all hidden neighbors must be safe
					elif num_mines_needed == 0:
						self.safe_cells.update(hidden_cells)

	def reveal_safe_cells(self):
		"""Reveal all cells that are guaranteed to be safe."""
		while self.safe_cells:
			row, col = self.safe_cells.pop()
			if self.board[row][col] == '?':
				self.to_explore.append((row, col))
				self.board[row][col] = 'S'  # Mark as safe

	def mark_mines(self):
		"""Mark all cells that are guaranteed to contain mines."""
		for (row, col) in self.mine_cells:
			if self.board[row][col] == '?':
				self.board[row][col] = 'M'  # Mark as mine

	def getAction(self, number: int) -> Action:
		"""
		Main function to decide the next action for the AI.
		Uses constraints to deduce the next move.
		"""
		if self.to_explore:
			row, col = self.to_explore.pop(0)
			return Action(AI.Action.UNCOVER, row, col)

		self.apply_constraints()
		self.reveal_safe_cells()
		self.mark_mines()

		if self.to_explore:
			row, col = self.to_explore.pop(0)
			return Action(AI.Action.UNCOVER, row, col)

		if self.mine_cells:
			row, col = self.mine_cells.pop()
			return Action(AI.Action.FLAG, row, col)

		return Action(AI.Action.LEAVE)  # If no moves left, leave the game
