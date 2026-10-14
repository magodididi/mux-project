class Mux4to1:
    def __init__(self, name="MUX", stuck_inputs=None, swap_inputs=None, stuck_outputs=None):
        self.name = name
        self.stuck_inputs = stuck_inputs or {}
        self.swap_inputs = swap_inputs or {}
        self.stuck_outputs = stuck_outputs

    def select(self, d0, d1, d2, d3, a0, a1):
        data = [d0, d1, d2, d3]
        data = [data[self.swap_inputs.get(i, i)] for i in range(4)]

        for i, value in self.stuck_inputs.items():
            data[i] = value

        na0 = 1 - a0
        na1 = 1 - a1

        y0 = na1 & na0 & data[0]
        y1 = na1 & a0 & data[1]
        y2 = a1 & na0 & data[2]
        y3 = a1 & a0 & data[3]

        y = y0 | y1 | y2 | y3

        if self.stuck_outputs is not None:
            y = self.stuck_outputs

        return y