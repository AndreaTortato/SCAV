
def rgb_to_yuv(r, g, b):
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -0.14713 * r - 0.288862 * g + 0.436 * b
    v = 0.615 * r - 0.51498 * g - 0.10001 * b
    return y, u, v


def yuv_to_rgb(y, u, v):
    r = y + 1.13983 * v
    g = y - 0.39465 * u - 0.5806 * v
    b = y + 2.03211 * u
    return r, g, b


# Example, one should return the other
print(rgb_to_yuv(100, 150, 200))
print(yuv_to_rgb(140.75, 29.16, -35.75))




