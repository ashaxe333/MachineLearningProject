def default_cl(gen, freq, is_gaming):
    """
    Assigns default CL (if not provided from title) to a ram based on ram generation, frequency and if its gaming/office
    :param gen: ram generation
    :param freq: ram frequency
    :param is_gaming: if ram is gaming
    :return: default CL value
    """
    if (gen == "DDR3" or gen == "DDR3L" or gen == 3) and freq < 1332:
        return 7 if is_gaming else 9
    elif (gen == "DDR3" or gen == "DDR3L" or gen == 3) and 1333 <= freq < 1866:
        return 9 if is_gaming else 11
    elif (gen == "DDR3" or gen == "DDR3L" or gen == 3) and 1867 <= freq:
        return 10 if is_gaming else 12
    elif (gen == "DDR4" or gen == 4) and freq < 2399:
        return 11 if is_gaming else 13
    elif (gen == "DDR4" or gen == 4) and 2400 <= freq < 2933:
        return 15 if is_gaming else 17
    elif (gen == "DDR4" or gen == 4) and 2934 <= freq < 3600:
        return 16 if is_gaming else 22
    elif (gen == "DDR4" or gen == 4) and 3601 < freq:
        return 18 if is_gaming else 26
    elif (gen == "DDR5" or gen == 5) and freq < 5599:
        return 32 if is_gaming else 40
    elif (gen == "DDR5" or gen == 5) and 5600 <= freq < 6399:
        return 36 if is_gaming else 42
    elif (gen == "DDR5" or gen == 5) and 6400 <= freq:
        return 38 if is_gaming else 46
    else:
        raise ValueError(f"Invalid ram generation, '{gen}' is not supported")

def default_voltage(gen, is_gaming):
    """
    Assigns default voltage (if not provided from title) based on ram generation and if its gaming/office
    :param gen: ram generation
    :param is_gaming: if ram is gaming
    :return: default voltage value
    """
    if gen == "DDR3" or gen == 3:
        return 1.6 if is_gaming else 1.5
    elif gen == "DDR3L" or gen == 3:
        return 1.35
    elif gen == "DDR4" or gen == 4:
        return 1.35 if is_gaming else 1.2
    elif gen == "DDR5" or gen == 5:
        return 1.25 if is_gaming else 1.1
    else:
        raise ValueError(f"Invalid ram generation, '{gen}' is not supported")

def default_gen(freq, capacity):
    """
    Assigns default generation based on ram generation and srequency
    :param freq: ram frequency
    :param capacity: ram capacity
    :return: ram generation
    """
    if freq < 2133:
        gen = 3
    elif freq < 4800:
        gen = 4
    else:
        gen = 5
    return gen