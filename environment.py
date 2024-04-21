"""This is a python library that will contain the environment class that will contain the minesweeper field."""
import numpy as np


class Unknown:
    def __init__(self, probability):
        self.probability = probability

    def __str__(self):
        return f"UKown({self.probability:.3f})"


class Known:
    def __init__(self, mines_around):
        self.mines_around = mines_around

    def __str__(self):
        return f"Known({self.mines_around:.3f})"


class Environment:
    """This class will contain the minesweeper field. The field is a matrix of cells."""

    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        initial_mine_probability = num_mines / (width * height)
        self.field = np.array(
            [np.array([Unknown(initial_mine_probability) for _ in range(height)]) for _ in range(width)])

    def __str__(self):
        stringbuilder = ""
        for y in range(self.height):
            for x in range(self.width):
                stringbuilder += str(self.field[x, y]) + "\t"
            stringbuilder += "\n"
        return stringbuilder

    def update_field(self, known_cells: list[(int, int, int)]) -> None:
        """This method will update the field with the new information.

        Args:
            known_cells: a list of coordinates and the number of mines around that cell.
        """
        for x, y, mines_around in known_cells:
            self.field[x, y] = Known(mines_around)
        for _ in range(self.width + self.height):  # run the update_probabilities method enough times to converge
            self.update_probabilities()

    def update_probabilities(self):
        """This method will update the probabilities of the unknown cells based on the known cells."""
        copy = self.field.copy()
        for x in range(self.width):
            for y in range(self.height):
                if isinstance(self.field[x, y], Unknown):
                    if copy[x, y].probability < 1.:  # if the probability is 1, then the cell is a mine
                        copy[x, y].probability = self.calculate_probability(x, y)
                        if copy[x, y].probability > 1.:
                            print(f"ERROR: Probability is greater than 1. ({x}, {y}, {copy[x, y].probability})")
                            exit()
        self.field = copy

    def calculate_probability(self, x, y) -> float:
        """This method will calculate the probability of a cell being a mine based on the known cells.

        Args:
            x: The x coordinate of the cell.
            y: The y coordinate of the cell.

        Returns:
            float: The probability of the cell being a mine.
        """
        if isinstance(self.field[x, y], Known):
            raise RuntimeError("calculate_probability() should only be called on unknown cells.")
        # check around the cell for knowns. If there are no known cells around the cell, return original probability.
        if self.field[x, y].probability == 1.:
            return 1.
        knowns_around = self.get_knowns_around(x, y)
        if len(knowns_around) == 0:
            num_of_unknowns = self.get_unknowns()
            num_of_mines_left = self.get_num_mines_left()
            return num_of_mines_left / (num_of_unknowns - 1) if num_of_unknowns > 1 else 1.

        # calculate the probability of the cell being a mine based on the known cells around it
        probabilities = [mines_around / unknowns_around if unknowns_around > 0. else 0. for
                         mines_around, unknowns_around in knowns_around]
        if max(probabilities) > 1.:
            print(f"ERROR: Probability is greater than 1. ({x}, {y}, {max(probabilities)}, {probabilities}, {knowns_around})")
            exit()
        return 0. if 0. in probabilities else max(probabilities)

    def get_unknowns(self) -> int:
        """This method will return the number of unknown cells in the field.

        Returns:
            int: The number of unknown cells in the f ield.
        """
        return np.sum(np.vectorize(lambda x: 1 if isinstance(x, Unknown) else 0)(self.field))

    def get_num_mines_left(self) -> int:
        """This method will return the number of mines left in the field.

        Returns:
            int: The number of mines left in the field.
        """
        return self.num_mines - np.sum(np.vectorize(lambda x: 1 if isinstance(x, Unknown) and x.probability == 1. else 0)(self.field))

    def get_knowns_around(self, x, y) -> list:
        """This method will return a list of known cells around a coordinate and the number of unknowns around those.

        Args:
            x: The x coordinate of the cell.
            y: The y coordinate of the cell.

        Returns:
            list: A list of known cells mines_around field around the coordinate and the number of unknowns around those.
        """
        knowns_around = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    if isinstance(self.field[x + dx, y + dy], Known):
                        knowns_around.append((
                            self.field[x + dx, y + dy].mines_around - self.get_presumed_mines_around(x + dx, y + dy),
                            self.get_unknowns_around(x + dx, y + dy)))
                        if knowns_around[-1][0] / knowns_around[-1][1] > 1.:
                            print(f"ERROR: Probability is greater than 1. ({x}, {y}, {self.field[x + dx, y + dy].mines_around} - {self.get_presumed_mines_around(x + dx, y + dy)}, {self.get_unknowns_around(x + dx, y + dy)})")
                            exit()
        return knowns_around

    def get_unknowns_around(self, x, y) -> int:
        """This method will return the number of unknown cells around a coordinate.

        Args:
            x: The x coordinate of the cell.
            y: The y coordinate of the cell.

        Returns:
            int: The number of unknown cells around the coordinate.
        """
        unknowns_around = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    if isinstance(self.field[x + dx, y + dy], Unknown) and self.field[x + dx, y + dy].probability < 1.:
                        unknowns_around += 1
        return unknowns_around

    def get_presumed_mines_around(self, x, y) -> int:
        """This method will return the number of presumed mines around a coordinate.

        Args:
            x: The x coordinate of the cell.
            y: The y coordinate of the cell.

        Returns:
            int: The number of presumed mines around the coordinate.
        """
        mines = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    if isinstance(self.field[x + dx, y + dy], Unknown) and self.field[x + dx, y + dy].probability == 1.:
                        mines += 1
        return mines

    def get_best_choices(self) -> (list, float):
        """This method will return unknown cells which have the lowest probability of being a mine and the probability.
        If there are multiple cells with the same probability, return all of them.

        Returns:
            list, float: A list of tuples containing the coordinates of the best choices and the probability.
        """
        probability_field = np.vectorize(lambda x: x.probability if isinstance(x, Unknown) else 1.)(self.field)
        min_coords = np.unravel_index(np.argmin(probability_field, axis=None), probability_field.shape)
        min_probability = probability_field[min_coords]
        ties = np.argwhere(probability_field == min_probability)
        ties = [tuple(tie) for tie in ties]
        return ties, min_probability
