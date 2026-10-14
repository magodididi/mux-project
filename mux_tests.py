from mux10to1 import Mux10to1


def bits(addr):
    return (
        addr & 1,
        (addr >> 1) & 1,
        (addr >> 2) & 1,
        (addr >> 3) & 1
    )

def call(device, data, addr):
    return device.select(data, *bits(addr))


def check(device, data, addr):
    expected = Mux10to1.golden(data, addr)
    actual = call(device, data, addr)
    return actual == expected


def test_T1(device):
    for addr in range(10):
        data = [0] * 10
        data[addr] = 1

        if not check(device, data, addr):
            return False

    return True


def test_T2(device):
    for addr in range(10):
        data1 = [0] * 10
        data2 = [1] * 10
        data2[addr] = 0

        if call(device, data1, addr) != call(device, data2, addr):
            return False

    return True


def test_T3(device):
    for addr in range(10):
        for value in (0, 1):
            data = [0] * 10
            data[addr] = value

            if not check(device, data, addr):
                return False

    return True


def test_T4(device):
    data = [1] * 10

    for addr in range(10, 16):
        if call(device, data, addr) != 0:
            return False

    return True


def test_T5(device):
    data = [0] * 10
    data[9] = 1

    return call(device, data, 9) == 1 and call(device, data, 10) == 0


def test_T6(device):
    for addr in range(10):
        data = [0] * 10

        if call(device, data, addr) != 0:
            return False

        data[addr] = 1

        if call(device, data, addr) != 1:
            return False

    return True


def test_T7(device):
    data = [1] * 10

    for addr in range(10):
        if call(device, data, addr) != 1:
            return False

    return True


def test_T8(device):
    data = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

    for addr in range(16):
        if not check(device, data, addr):
            return False

    return True


def test_T9(device):
    data = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

    for addr in range(10):
        if call(device, data, addr) != data[addr]:
            return False

    return True


def run_tests(device):
    tests = [
        ("T1", test_T1),
        ("T2", test_T2),
        ("T3", test_T3),
        ("T4", test_T4),
        ("T5", test_T5),
        ("T6", test_T6),
        ("T7", test_T7),
        ("T8", test_T8),
        ("T9", test_T9)
    ]

    passed = 0

    for test_id, test in tests:
        result = test(device)

        if result:
            passed += 1
            print(f"{test_id}: ок")
        else:
            print(f"{test_id}: ошибка")

    print(f"Итого: {passed}/{len(tests)}")

    return passed == len(tests)


def test_faults():
    faults = [
        ("E1", "d5 залип в 0", {"M2_stuck_in": {1: 0}}),
        ("E2", "d2 залип в 1", {"M1_stuck_in": {2: 1}}),
        ("E3", "перепутаны d0 и d1", {"M1_swap_in": {0: 1, 1: 0}}),
        ("E4", "a2 залип в 0", {"addr_stuck": {2: 0}}),
        ("E5", "перепутаны a0 и a1", {"addr_swap": {0: 1, 1: 0}}),
        ("E6", "выход MUX3 залип в 0", {"M3_stuck_out": 0}),
        ("E7", "выход MUX4 залип в 1", {"M4_stuck_out": 1}),
        ("E9", "плавающий d7", {"floating_inputs": {7}})
    ]

    tests = [
        ("T1", test_T1),
        ("T2", test_T2),
        ("T3", test_T3),
        ("T4", test_T4),
        ("T5", test_T5),
        ("T6", test_T6),
        ("T7", test_T7),
        ("T8", test_T8),
        ("T9", test_T9)
    ]

    for fault_id, name, fault in faults:
        device = Mux10to1(fault)
        detected = []

        for test_id, test in tests:
            if not test(device):
                detected.append(test_id)

        if detected:
            print(f"{fault_id}: {name} — найден")
            print(f"Тесты: {', '.join(detected)}")
        else:
            print(f"{fault_id}: {name} — не найден")


def test_noise(total=1000):
    device = Mux10to1({"noise_prob": 0.1})

    data = [0] * 10
    data[0] = 1

    errors = 0

    for _ in range(total):
        if call(device, data, 0) != 1:
            errors += 1

    percent = errors / total * 100

    print(f"E8: ошибок {errors}/{total} ({percent:.1f}%)")