def check_triangle(a, b, c):
    s = [a, b, c]
    for x in s:
        if (not isinstance(x, int)) and (not isinstance(x, float)):
            return False
        if x <= 0:
            return False
    return a + b > c and b + c > a and a + c > b
