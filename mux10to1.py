import random
from mux4to1 import Mux4to1


class Mux10to1:
    def __init__(self, faults=None):
        faults = faults or {}

        self.mux1 = Mux4to1(
            "MUX1",
            stuck_inputs=faults.get("M1_stuck_in"),
            swap_inputs=faults.get("M1_swap_in"),
            stuck_outputs=faults.get("M1_stuck_out")
        )

        self.mux2 = Mux4to1(
            "MUX2",
            stuck_inputs=faults.get("M2_stuck_in"),
            swap_inputs=faults.get("M2_swap_in"),
            stuck_outputs=faults.get("M2_stuck_out")
        )

        self.mux3 = Mux4to1(
            "MUX3",
            stuck_inputs=faults.get("M3_stuck_in"),
            swap_inputs=faults.get("M3_swap_in"),
            stuck_outputs=faults.get("M3_stuck_out")
        )

        self.mux4 = Mux4to1(
            "MUX4",
            stuck_inputs=faults.get("M4_stuck_in"),
            swap_inputs=faults.get("M4_swap_in"),
            stuck_outputs=faults.get("M4_stuck_out")
        )

        self.addr_stuck = faults.get("addr_stuck", {})
        self.addr_swap = faults.get("addr_swap", {})
        self.floating_inputs = faults.get("floating_inputs", set())
        self.noise_prob = faults.get("noise_prob", 0.0)

    def _apply_addr_faults(self, a0, a1, a2, a3):
        bits = [a0, a1, a2, a3]

        for i, value in self.addr_stuck.items():
            bits[i] = value

        for i, j in self.addr_swap.items():
            bits[i], bits[j] = bits[j], bits[i]

        return bits

    def _apply_data_faults(self, data):
        data = list(data)

        for i in self.floating_inputs:
            if 0 <= i < 10:
                data[i] = random.randint(0, 1)

        return data

    def select(self, data, a0, a1, a2, a3):
        data = self._apply_data_faults(data)
        a0, a1, a2, a3 = self._apply_addr_faults(a0, a1, a2, a3)

        y0 = self.mux1.select (data[0], data[1], data[2], data[3], a0, a1)

        y1 = self.mux2.select(data[4], data[5], data[6], data[7], a0, a1)

        y2 = self.mux3.select(data[8], data[9], 0, 0, a0, a1)

        y = self.mux4.select(y0, y1, y2, 0, a2, a3)

        if random.random() < self.noise_prob:
            y ^= 1

        return y

    @staticmethod
    def golden(data, addr):
        if 0 <= addr <= 9:
            return data[addr] & 1
        return 0