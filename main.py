from mux10to1 import Mux10to1
from mux_tests import run_tests, test_faults, test_noise


device = Mux10to1()

run_tests(device)
test_faults()
test_noise()