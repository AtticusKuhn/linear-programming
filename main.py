from ortools.linear_solver import pywraplp
from math import log
size= 3

def fmt(i,j,k):
    return f"{i}-{j}-{k}"


def main():
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # create variables
    x = {}
    for i in range(size):
        for j in range(size):
            for k in range(size**2):
                x[fmt(i, j, k)] =  solver.IntVar(0, 1, f"x_{fmt(i, j, k)}")
    print('Number of variables =', solver.NumVariables())
    # constraint number 1 each square must have exactly 1 number written in it
    for i in range(size):
        for j in range(size):
            constraint = solver.RowConstraint(0,1, '')
            for k in range(size**2):
                constraint.SetCoefficient(x[fmt(i, j, k)], 1)
    # contraint number 2 all numbers must appear in the grid exactly once
    for k in range(size**2):
        constraint = solver.RowConstraint(0, 1, '')
        for i in range(size):
            for j in range(size):
                constraint.SetCoefficient(x[fmt(i, j, k)], 1)
    #constraint number 3 products must be equal
    for t in range(size):
        constraint = solver.RowConstraint(0, 0, '')
        for i in range(size):
            for j in range(size):
                for k in range(size**2):
                    print("setting",fmt(t, j, k))
                    print("setting",fmt(i,t,k))
                    constraint.SetCoefficient(x[fmt(t, j, k)], log(k+1))
                    constraint.SetCoefficient(x[fmt(i, t, k)], -log(k+1))
        # for j in range(size):
        #     for k in range(size**2):
        #         constraint.SetCoefficient(x[fmt(t, j, k)], log(k+1))
        # for i in range(size):
        #     for k in range(size**2):
        #         constraint.SetCoefficient(x[fmt(i, t, k)], -log(k+1))





    
    # for i in range(data['num_constraints']):
    #     constraint = solver.RowConstraint(0, data['bounds'][i], '')
    #     for j in range(data['num_vars']):
    #         constraint.SetCoefficient(x[j], data['constraint_coeffs'][i][j])
    print('Number of constraints =', solver.NumConstraints())
    # In Python, you can also set the constraints as follows.
    # for i in range(data['num_constraints']):
    #  constraint_expr = \
    # [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    #  solver.Add(sum(constraint_expr) <= data['bounds'][i])

    objective = solver.Objective()
    for i in range(size):
        for j in range(size):
            for k in range(size**2):     
                objective.SetCoefficient(x[fmt(i, j, k)],100)
    objective.SetMaximization()
    # In Python, you can also set the objective as follows.
    # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
    # solver.Maximize(solver.Sum(obj_expr))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Objective value =', solver.Objective().Value())
        # for i in range(size):
        #     for j in range(size):
        #         for k in range(size**2):     
        #             print(x[fmt(i, j, k)].name(), ' = ', x[fmt(i, j, k)].solution_value())
        for i in range(size):
            print()
            for j in range(size):
                print(" ", end="")
                for k in range(size**2):
                    if x[fmt(i, j, k)].solution_value() ==1 :
                        print(k+1, end="")
        print()
        print('Problem solved in %f milliseconds' % solver.wall_time())
        print('Problem solved in %d iterations' % solver.iterations())
        print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    else:
        print('The problem does not have an optimal solution.')


if __name__ == '__main__':
    main()
 