import math
import random
import tkinter

# ____________________________________________________________________________________________________
# This genetic algorithm interfaces with John Conway's Game of life And with that it provides ground
# for the creation of a huge variety of forms such as Methuselahs,Guns,Oscillators and more...

# click on any cell that you like and get info about it such that his x,y values on the grid ,
# his current state LIFE/DEATH , his living neighbours and his special String as a candidate of being an
# Organism center.
# ____________________________________________________________________________________________________


TOTAL_FITNESS_DATA = []


# an object that will represent a live organism that will contain initially at least 20 live cells
class Organism:
    def __init__(self, org_str, tot_live_cells):
        self.org_str = org_str
        self.tot_live_cells = tot_live_cells
        # we will define fitness as a value from 0 to 1 which 0 is min fit and 1 is max fit
        # we will calculate the fitness of this organism according to his live cells span
        # as a function of his total live cells
        # we base are definition of high fitness level on the fact that if we are created this object
        # that means we have at least 20 live cells and the degree of span is the key here
        # we will count the "space" between the live cells
        tmp_str = self.org_str
        # s will hold a list of separated 1's from the 0's ,longer list == good span of cells == High birth chance
        s = tmp_str.split('0')
        # we will subtract the empty cells from the list length and left with the number of separated 1's
        cnt = len(s) - s.count('')
        # we will implement the division of joined 1's by the total number of them and get the fitness of this organism
        self.fitness = cnt / self.tot_live_cells


class Cell:
    def __init__(self, grid, x, y, _type):
        self.grid = grid
        self.x = x
        self.y = y
        self.type = _type
        self.organism = None
        self.MIN_ORG_LIVE_CELLS = 20
        self.live_neighbours = 0
        self.str_neighbours = ""

        self.next_type = self.type

    def exec(self):
        self.type = self.next_type

    def calc_next_gen_this_cell(self):
        (org_str, cnt_neig, tot_live_cells) = self.grid.get_neighbours(self.x, self.y, self.type)

        self.live_neighbours = cnt_neig
        self.str_neighbours = org_str

        if self.type == "LIFE":
            self.grid.total_live_cnt += 1

        if self.live_neighbours < 2 or self.live_neighbours > 3:
            self.next_type = "DEATH"

        elif self.live_neighbours == 3 and self.type == "DEATH":
            self.next_type = "LIFE"

        # An organism creation conditions
        if tot_live_cells >= self.MIN_ORG_LIVE_CELLS and self.grid.cycle_org == 0:
            self.organism = Organism(org_str, tot_live_cells)
            self.grid.cycle_org += 1
            pass

        # it takes the (length of the grid * 2.5) cycles from the old organism creation for creating a new one
        if self.grid.cycle_org > 0:
            self.grid.cycle_org = (self.grid.cycle_org + 1) % (self.grid.length * 2.5)

    def get_color(self):
        if self.type == "DEATH":
            return "black"
        else:  # if LIFE
            if (self.grid.Stage % 7) == 0:
                return random.choice(["green2", "green3", "green4"])
            if (self.grid.Stage % 7) == 1:
                return random.choice(["turquoise1", "turquoise2", "turquoise3"])
            if (self.grid.Stage % 7) == 2:
                return random.choice(["red2", "red3", "red4"])
            if (self.grid.Stage % 7) == 3:
                return random.choice(["yellow2", "yellow3", "yellow4"])
            if (self.grid.Stage % 7) == 4:
                return random.choice(["purple2", "purple3", "purple4"])
            if (self.grid.Stage % 7) == 5:
                return random.choice(["blue2", "blue3", "blue4"])
            if (self.grid.Stage % 7) == 6:
                return random.choice(["ivory2", "ivory3", "ivory4"])


class Grid:
    def __init__(self, length, conf_sz, cycle_gen):
        self.length = length
        self.config_size = conf_sz
        self.cells = self.create_cells()
        self.Generation = 0
        self.cycle_gen = cycle_gen
        self.Stage = 0
        self.org_set = set()  # will hold org's from every gen
        self.org_fit_set = set()  # will hold the best fitted org's from this stage
        self.cycle_org = 0  # a helper attribute for organism creator
        self.total_live_cnt = 0

    def exec_new_stage(self):
        self.Generation = 0
        self.cycle_org = 0
        self.Stage += 1

        # inserting the new organism to our grid and clear the fit_set for the next iteration
        self.insert_new_organism(self.select())
        self.org_fit_set.clear()

    # our organism selection process base on the Genetic algorithm of Roulette wheel selection.
    # we will sum all the fitness values together and each individual will have a chance to be
    # selected based on its fitness level divided by the total fitness sum
    def select(self):
        total_fitness = sum(map(lambda x: x.__getattribute__("fitness"), self.org_fit_set))
        wheel_location = random.uniform(0, 1) * total_fitness

        org = self.org_fit_set.pop()
        curr_sum = org.__getattribute__("fitness")
        while len(self.org_fit_set) > 0 and curr_sum < wheel_location:
            org = self.org_fit_set.pop()
            curr_sum = org.__getattribute__("fitness")
        return org

    def insert_new_organism(self, org):
        x = random.randint(0, self.length - 1)
        y = random.randint(0, self.length - 1)
        org_str = org.__getattribute__("org_str")
        _len = len(org_str)

        for i in range(math.floor(_len ** 0.5)):
            for j in range(math.floor(_len ** 0.5)):
                t = "LIFE" if org_str[(i * math.floor(_len ** 0.5)) + j] == '1' else "DEATH"
                self.cells[(x + i) % self.length][(y + j) % self.length].__setattr__("type", t)

    def exec_new_gen(self):
        if self.Generation == self.cycle_gen:
            self.exec_new_stage()

        self.Generation += 1

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].calc_next_gen_this_cell()

                curr_org = self.cells[x][y].__getattribute__("organism")
                if curr_org is None:
                    continue
                self.org_set.add(curr_org)

        for x in range(self.length):
            for y in range(self.length):
                self.cells[x][y].exec()

        # adding the current live cells count to the list and set the count to zero again
        TOTAL_FITNESS_DATA.append(self.total_live_cnt)
        self.total_live_cnt = 0

        # find and extract the best fit organism from this gen
        _MAX = self.org_set.pop()
        for i in self.org_set:
            if i.__getattribute__("fitness") > _MAX.__getattribute__("fitness"):
                _MAX = i

        if _MAX is None:
            return
        # if we indeed found some organism, we add it to the fit set and clear the org_set
        self.org_fit_set.add(_MAX)
        self.org_set.clear()

    # A function that build an individual organism centered on (x,y) input
    def get_neighbours(self, x, y, _type):
        org_str = ""  # will hold a string that represent the whole individual organism
        tot_live_cells = 0 if _type == "DEATH" else 1  # count the live cells in this individual
        cnt_live_neig = 0  # count the direct live neighbours
        # get all of its (7X7-1) neighbours, get the organism string
        for i in range(-3, 4):
            for j in range(-3, 4):
                if (i, j) == (0, 0):
                    org_str += '0' if _type == "DEATH" else '1'
                    continue

                curr_neig_type = self.cells[((x + i) % self.length)][((y + j) % self.length)].__getattribute__("type")

                if curr_neig_type == "LIFE":
                    tot_live_cells += 1
                    org_str += '1'
                    if (-2 < j) and (j < 2) and (-2 < i) and (i < 2):
                        cnt_live_neig += 1
                else:
                    org_str += '0'

        return org_str, cnt_live_neig, tot_live_cells

    def create_cells(self):
        cells = [[0 for i in range(self.length)] for j in range(self.length)]
        center = int(math.floor(self.length / 2))
        pivot = int(math.floor(self.config_size ** 0.5))

        for x in range(self.length):
            for y in range(self.length):
                if (center + pivot) >= x >= (center - pivot) and (center + pivot) >= y >= (center - pivot):
                    cells[x][y] = Cell(self, x, y, _type=random.choice(["LIFE", "DEATH"]))
                else:
                    cells[x][y] = Cell(self, x, y, _type="DEATH")

        return cells


class App:
    def __init__(self, deadline, length, init_conf_size, cycle_gen, cell_size, refresh_rate):
        self.length = length
        self.cell_size = cell_size
        self.refresh_rate = refresh_rate
        self.init_conf_size = init_conf_size
        self.deadline = deadline

        self.items = [[0 for i in range(self.length)] for j in range(self.length)]

        self.grid = Grid(self.length, self.init_conf_size, cycle_gen)
        self.root = tkinter.Tk()
        self.root.title("Genetic Algorithm - Game Of Life - Tommy Ashkenazi")

        self.label = tkinter.Label(self.root)
        self.label.pack()

        self.canvas = tkinter.Canvas(self.root, width=self.length * self.cell_size,
                                     height=self.length * self.cell_size)

        self.canvas.pack()

        self.items = self.update_canvas(self.items)

        self.root.after(self.refresh_rate, self.refresh_window)
        self.root.mainloop()

    def refresh_window(self):
        if self.grid.Stage < self.deadline:
            self.grid.exec_new_gen()

        self.update_canvas(canv_items=self.items, canv_done=True)
        self.canvas.bind('<Button-1>', self.click_cell_info)
        self.root.after(self.refresh_rate, self.refresh_window)
        self.label.config(text="Stage {}        Generation {}/{}"
                          .format(self.grid.Stage, self.grid.Generation, self.grid.cycle_gen))

    def update_canvas(self, canv_items, canv_done=False):
        cell_items = self.grid.cells

        if not canv_done:
            for x in range(len(cell_items)):
                for y in range(len(cell_items)):
                    cell = cell_items[x][y]

                    rect_id = self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                                           (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                                           fill=cell.get_color())

                    canv_items[x][y] = rect_id

            return canv_items
        else:
            for x in range(len(canv_items)):
                for y in range(len(canv_items)):
                    cell = cell_items[x][y]
                    rect_id = canv_items[x][y]
                    self.canvas.itemconfig(rect_id, fill=cell.get_color())

    # we can click on any cell on the window and get info about it
    def click_cell_info(self, event):
        _x = math.floor(event.__getattribute__('x') / self.cell_size)
        _y = math.floor(event.__getattribute__('y') / self.cell_size)
        cell = self.grid.cells[_x][_y]
        print("<[x={},y={}] , {} , live_neig {} , nieg_str {} , total live cells {}>"
              .format(_x, _y, cell.__getattribute__("type"),
                      cell.__getattribute__("live_neighbours"),
                      cell.__getattribute__("str_neighbours"),
                      TOTAL_FITNESS_DATA[len(TOTAL_FITNESS_DATA) - 1]))


# from here we launch the program , you can define the values as you like
if __name__ == '__main__':
    app = App(deadline=1000, length=40, init_conf_size=25, cycle_gen=20, cell_size=16, refresh_rate=1)

    file = open("gen_fitness.txt", 'w')
    for i in TOTAL_FITNESS_DATA:
        file.write("{}\n".format(i))
    file.close()
