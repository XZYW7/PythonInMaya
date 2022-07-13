from opensimplex import OpenSimplex
gen = OpenSimplex(5)#要输入数据
def noise(nx, ny):
    # Rescale from -1.0:+1.0 to 0.0:1.0
    return gen.noise2(nx, ny) / 2.0 + 0.5

height=10
width=10

value = []
for y in range(height):
    value.append([0] * width)
    for x in range(width):
        nx = x/width - 0.5
        ny = y/height - 0.5
        value[y][x] = noise(nx, ny)
print(value)