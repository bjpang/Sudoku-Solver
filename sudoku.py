import random

def crossover(X, Y):
    """Creates a list that crosses and adds the values in X and Y"""
    return [x + y for x in X for y in Y]

def evalPuzzle(puzzle, squares):
    """Takes in a puzzle string and creates a respective dictionary.
       The dictionary has a single value or multiple depending on if it is empty or not."""

    values = {}
    puzzle.split('\n')
    counter = 0
    for line in puzzle:
        for val in line:
            if val.isdigit() or val == '.':
                if val == '.':
                    values[squares[counter]] = "123456789"
                else:
                    values[squares[counter]] = str(val)
                counter += 1
    return values

def constraint(values, neighbors, squares):
    """Constraints the values in the neighbors of squares that already have values"""
    for square in squares:
        val = values[square]
        if len(val) == 1:
            for neighbor in neighbors[square]:  
                values[neighbor] = values[neighbor].replace(val, '')
                if len(values[neighbor]) == 0:
                    return False
    return values

def searchValues(values, neighbors, squares):
    if values == False:
        return False
    if all(len(values[s]) == 1 for s in squares): 
        return values

    mrvlen, mrv = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
   
    for x in range(0, mrvlen):
        tempvalues = values.copy()
        tempvalues[mrv] = str(values[mrv][x])
        tempvalues = constraint(tempvalues, neighbors, squares)
        if tempvalues != False:
            finalvalues = searchValues(tempvalues, neighbors, squares)
            if finalvalues != False:
                return finalvalues
    return False


def puzzleAsString(values):
    puzzle = ""
    counter = 1
    counter2 = 0
    for square in sorted(values):
        if counter == 10:
            puzzle += "\n"
            counter2 += 1
            if counter2 == 3 or counter2 == 6:
                puzzle += "------+------+------\n"
            counter = 1
        counter += 1
        puzzle += str(values[square]) + " "
        if counter % 3 == 1 and counter != 10:
            puzzle += '|'
    return puzzle


if __name__ == "__main__":
    f = open('sudoku.txt', 'w')

    """Creates all the rows, columns, and grids for sudoku
       Columns are 1-9
       Rows are A-I"""
    digits = "123456789"
    letters = "ABCDEFGHI"
    squares = crossover(letters, digits)
    columns = [crossover(letters, d) for d in digits]
    rows = [crossover(l, digits) for l in letters]
    grid = [crossover(l, d) for l in (letters[:3], letters[3:6], letters[6:])
                            for d in (digits[:3], digits[3:6], digits[6:])]
    RCG = rows + columns + grid
    units = dict((s, [u for u in RCG if s in u]) for s in squares)
    neighbors = dict((s, set(sum(units[s],[])) - set([s])) for s in squares)

    puzzle = """
             6 . 4 |. . 2 |1 . . 
             1 . 2 |. . 7 |4 . . 
             . 3 . |. . . |2 6 . 
             ------+------+------
             3 . 8 |6 1 4 |7 . . 
             4 6 . |2 . . |. 5 1 
             . . 1 |9 5 8 |. 3 4 
             ------+------+------
             9 . . |. . 5 |. 4 . 
             2 7 . |1 . . |. 8 6 
             . . . |7 3 . |. 1 2 
             """

    values = evalPuzzle(puzzle, squares)

    values = constraint(values, neighbors, squares)    


    values = searchValues(values, neighbors, squares)

    if values == False:
        print "Puzzle is unsolvable. Apologies."
    else:
        puz = puzzleAsString(values)

    f.write(puz)