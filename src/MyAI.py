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


		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################
