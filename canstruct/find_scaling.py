import math

def find_scaling(min_value, max_value, number_of_bits):
    max_int = float(math.pow(2, number_of_bits))-1
    eng_range = max_value - min_value
    scale = eng_range/max_int
    offset = min_value
    print "offset:", offset
    print "scale:", scale
    '''
    print " ---- test ----"
    for point in range(10):
        x = (point/9.0) * (max_value - min_value) + min_value
        y = (x - offset) / scale
        print "engineering {}  ===   raw {}".format(x, y)
    '''
    print " ---- test ----"
    for point in range(10):
        x = int((point/9.0) * (max_int))
        x = float(x)
        y = (x * scale) + offset
        print "raw {}  === eng {}".format(x, y)


