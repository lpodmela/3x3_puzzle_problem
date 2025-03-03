import heapq
from tkinter import *
from tkinter import messagebox

# hardest starting matrix, minimum of steps == 31
STARTING_MATRIX = [
    [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]
]

FINAL_MATRIX =  [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# list of possible moves of zero
POSSIBLE_MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# function to find the zero in the matrix and also for manhattan heuristics
def find_index(matrix, number):
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == number:
                return i,j
            
# creating new matrix with swapped given numbers
def swap(matrix, pos_1, pos_2):
    x1, y1 = pos_1
    x2, y2 = pos_2
    new_state = [row[:] for row in matrix]
    new_state[x1][y1], new_state[x2][y2] = new_state[x2][y2], new_state[x1][y1]
    return new_state

# creating list of possible matrixs by swapping by possible moves of 0
def get_neighbours(state):
    neighbours = []
    x_zero, y_zero = find_index(state, 0)
    
    for move_x, move_y in POSSIBLE_MOVES:
        pos_x, pos_y = move_x + x_zero, move_y + y_zero
        # checking if the coords of index are in the limit of 3x3 matrix (indexing from 0 to 2)
        if 0 <= pos_x < 3 and 0 <= pos_y < 3:
            neighbours.append(swap(state, (x_zero, y_zero), (pos_x, pos_y)))
    return neighbours


def is_solvable(matrix):
    
    # Flatten the matrix into a single list, ignoring the zero
    flat_list = []
    for row in matrix:
        for num in row:
            if num != 0:
                flat_list.append(num)

    # Count the number of inversions
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1

    # Return True if the number of inversions is even
    return inversions % 2 == 0

# comparing index of actual state with final matrix, difference is added to man_num, smallest man_number of possible matrix moves wins 
def manhattan(state):
    man_num = 0
    for number in range(1,9):
        index_final = find_index(FINAL_MATRIX, number)
        index_state = find_index(state, number)

        man_num += abs(index_final[0] - index_state[0]) + abs(index_final[1] - index_state[1])
        
    return man_num

# astar algorithm
def astar(start_matrix):
    
    if not is_solvable(start_matrix):
        return None, 0

    expanded_nodes = 0
    closed_set = {}
    open_set = []
    heapq.heappush(open_set,(0,start_matrix))
    g_score = {str(start_matrix) : 0}
    h_score = manhattan(start_matrix)
    f_score = {str(start_matrix) : h_score}

    while open_set:
        _, current = heapq.heappop(open_set)
        expanded_nodes += 1

        if current == FINAL_MATRIX:
            return path_reconstruct(closed_set, current), expanded_nodes
        
        for each in get_neighbours(current):
            current_g_score = g_score[str(current)] + 1
            neighbour_str = str(each)

            if neighbour_str not in g_score or current_g_score < g_score[neighbour_str]:
                closed_set[neighbour_str] = current
                g_score[neighbour_str] = current_g_score
                f_score[neighbour_str] = current_g_score + manhattan(each)
                heapq.heappush(open_set,(f_score[neighbour_str], each))
    return None, expanded_nodes

def path_reconstruct(came_from, current):
    path = [current]

    while str(current) in came_from:
        current = came_from[str(current)]
        path.append(current)
    return path[::-1]

class PuzzleVisualizer(Tk):
    def __init__(self, path, expanded_nodes):
        super().__init__()
        self.title("8-Puzzle")
        self.path = path
        self.step = 0
        self.expanded_nodes = expanded_nodes
        self.create_widgets()
        
        if self.path is None:
            self.start_button.config(state=DISABLED)
            self.pop_up()

        self.mainloop()


    def create_widgets(self):
        # 3x3 grid
        self.buttons = [[Button(self, text=STARTING_MATRIX[i][j], width=6, height=3, font=('Arial', 24)) 
                         for j in range(3)] for i in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j].grid(row=i, column=j)

        # Start button
        self.start_button = Button(self, text="Start Solving", command=self.path_printer)
        self.start_button.grid(row=3, column=0, columnspan=3)

    def path_printer(self):
        self.start_button.config(state=DISABLED)
        self.auto_step()

        for step_number, step in enumerate(self.path):
            print(f"Step {step_number}")
            for row in step:
                print(row)
            print("")
    
    def pop_up(self):
        if self.path is None:
            messagebox.showinfo(title = "Error", message = "Starting matrix does not have solution.\nChange value of the matrix.")
        else:
            messagebox.showinfo(title = "Solution found", message = f"Each step of this solution is written in the terminal.\nNumber of steps: {self.step}\nExpanded nodes: {self.expanded_nodes}")

    def display_step(self):
        # Update the buttons with the current puzzle state
        state = self.path[self.step]
        for i in range(3):
            for j in range(3):
                num = state[i][j]
                self.buttons[i][j].config(text=num)

    def auto_step(self):
        # Move to the next step automatically
        if self.step < len(self.path) - 1:
            self.step += 1
            self.display_step()
            self.after(1000, self.auto_step)  # Call the function again after 1000ms
        else:
            self.pop_up()
    
    

if __name__ == "__main__":
    path, expanded_nodes = astar(STARTING_MATRIX)
    app = PuzzleVisualizer(path,expanded_nodes)






        


