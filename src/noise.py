'''
    This code uses other people's implementation of perlin noise
'''
import numpy
#import cv2

def lerp(y1,y2,w):

    return y1 + (y2 - y1) * w

def twist(x):
    # 3t^2 - 2t^3

    return x**2 * (3 - 2 * x)

def twist2(x):
    # 6t^5 - 15t^3 + 10t^3

    return x**3 * (6 * x**2 - 15 * x + 10)

class ImageData:
    ''' represent an image file '''

    def __init__(self,size=(512,512)):
        self.__image = numpy.ndarray(size)

    def draw_point(self,position:tuple,value:int):
        '''set pixel of target position with given value
        @position: like (x, y)
        @value: a float value between 0 and 1'''

        self.__image[position[1]][position[0]] = value

    #def save(self,filepath:str):
        ''' write image to local file '''

       # cv2.imwrite(filepath, self.__image)


class PerlinNoise2D:

    def __init__(self,latticeLength=64,latticeCount=8):
        '''latticeLength means the side length of a single lattice
        both x and y. and each value will be scaled to 1 '''

        self.lattice_length = latticeLength
        self.lattice_count = latticeCount

    def scaled_pos(self,value:int):
        ''' scaled a position to 0 - 1'''

        return value/self.lattice_length - value//self.lattice_length

    def __generate_random_lattice(self):
        ''' generate lattice^2 random gradients '''

        count = self.lattice_count + 1
        gradients = [[numpy.random.randint(-255,255,size=(2, )) for x in range(count)] for y in range(count)]
        self.gradients = numpy.array(gradients)

        heights = [[numpy.random.randint(50, 100) for x in range(count)] for y in range(count)]
        self.heights = numpy.array(heights)

    def noise(self):

        size = self.lattice_length * self.lattice_count
        image = ImageData(size=(size, size))
        self.__generate_random_lattice()
        for ly in range(self.lattice_count):
            for lx in range(self.lattice_count):
                for y in range(self.lattice_length):
                    for x in range(self.lattice_length):
                        u,v = self.scaled_pos(x),self.scaled_pos(y)
                        pos0 = numpy.array([u, v])
                        pos1 = numpy.array([u - 1, v])
                        pos2 = numpy.array([u, v - 1])
                        pos3 = numpy.array([u - 1, v - 1])

                        grad0 = self.gradients[lx, ly]
                        grad1 = self.gradients[lx + 1, ly]
                        grad2 = self.gradients[lx, ly + 1]
                        grad3 = self.gradients[lx + 1, ly + 1]

                        w1,w2 = twist2(u),twist2(v)
                        z1 = numpy.dot(pos0, grad0) + self.heights[lx, ly]
                        z2 = numpy.dot(pos1, grad1) + self.heights[lx + 1, ly]
                        z3 = numpy.dot(pos2, grad2) + self.heights[lx, ly + 1]
                        z4 = numpy.dot(pos3, grad3) + self.heights[lx + 1, ly + 1]

                        l1 = lerp(z1, z2, w1)
                        l2 = lerp(z3, z4, w1)
                        noise = lerp(l1, l2, w2)
                        image.draw_point((x + lx * self.lattice_length, y + ly * self.lattice_length), noise )

        return image
                

x = PerlinNoise2D(latticeLength=64,latticeCount=8)
x.noise().save("./test.png")

'''
不用cv2生成图片的方法
def main():
    print('Generating 2D image...')
    im = Image.new('L', (WIDTH, HEIGHT))
    for y in range(0, HEIGHT):
        for x in range(0, WIDTH):
            value = simplex.noise2(x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = int((value + 1) * 128)
            im.putpixel((x, y), color)
    im.save('noise2d.png')
'''