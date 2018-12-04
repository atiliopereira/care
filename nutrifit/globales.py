def separar(x):
    if type(x) not in [type(0), type(0)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + separar(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ".%03d%s" % (r, result)
    return "%d%s" % (x, result)

NOMBRE_EMPRESA = 'NUTRIFIT'
