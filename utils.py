def calc_flowrate(x, a=0.00014933173223849661, b=1.6854748802635457):
    """
    :param x: height difference between water surface and juicer mouth piece
    :param a: coefficient
    :param b: coefficient
    :return: a*x**b
    """
    return a*x**b