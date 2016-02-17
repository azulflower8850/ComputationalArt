

""" Kevin Zhang's Computational Art - uses recursion to build a random function, which is then put into an image processing algorithm to produce 'art'
    Also implemented a third variable t to increment the pictures and compiled them into a movie of 'art'
 """

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)




        I believe that doctests on this are impossible because the function is completely randomized.
        The best I can do is check to see that the function is representing itself correctly with
        some manual testing.
    """





    """
    random_depth = random.randint(min_depth-1, max_depth-1)

    if random_depth <= 0:

        return random.choice(["x", "y"])

    else:

        random_number = random.randint(1,6)

        if random_number == 1: #prod(a,b) = ab
            return ["prod", build_random_function(min_depth-1,max_depth-1), build_random_function(min_depth-1,max_depth-1)]

        elif random_number == 2: #avg(a,b) = .5 * (a+b)
            return  ["avg", build_random_function(min_depth-1,max_depth-1), build_random_function(min_depth-1,max_depth-1)]

        elif random_number == 3: #cos_pi(a) = cos(pi*a)
            return ["cos_pi", build_random_function(min_depth-1,max_depth-1)]

        elif random_number == 4:  #sin_pi(a) = sin(pi*a)
            return ["sin_pi", build_random_function(min_depth-1, max_depth-1)]         

        elif random_number == 5:   #square(a) = a**2
            return ["square", build_random_function(min_depth-1, max_depth-1)]

        elif random_number == 6:    #absolute_diff(a) = abs(a)-abs(b)
            return ["absolute_diff", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]          
        """    



    #Defining all my lambda functions

    prod = lambda x,y,t: x * y
    avg = lambda x,y,t: .5 * (x + y)
    cos_pi = lambda x: math.cos(math.pi * x)
    sin_pi = lambda x: math.sin(math.pi * x)
    square = lambda x: x ** 2
    absdiff = lambda x,y,t: abs(x) - abs(y)
    time = lambda x,y,t: t
    x = lambda x,y,t: x
    y = lambda x,y,t: y
    


    #Randomly choosing my function

    funcs = [prod, avg, cos_pi, sin_pi, square, absdiff, time]
    func = random.choice(funcs)

    #Randomly choosing depth

    random_depth = random.randint(min_depth-1, max_depth-1)

    #Base Case

    if random_depth <=0:

        newfunc = random.choice([x(x,y,time), y(x,y,time), time(x,y,time)])  #This part works, but it's jank, as vouched by Patrick

     #Generating the function, using recursion and based on whether it takes one argument or two   

    elif func in [prod, avg, absdiff, x, y, time]:

        func1 = build_random_function(min_depth-1, max_depth-1)
        func2 = build_random_function(min_depth-1, max_depth-1)
        newfunc = lambda x,y,t: func(func1(x,y,t), func2(x,y,t), time(x,y,t))

    else:

        singlefunc = build_random_function(min_depth-1, max_depth-1)
        newfunc = lambda x,y,t: func(singlefunc(x,y,t))


    return newfunc        

    





def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02


        Some more testing to ensure functionality
        >>> evaluate_random_function(["sin_pi",["x"]],0,1)
        0.0
        >>> evaluate_random_function(["prod", ["cos_pi", ["x"]], ["prod", ["square",["y"]],["absolute_diff", ["x"], ["y"]]]], 0, 1)
        -1.0
    """
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    else:
        if(f[0] == "prod"):      #performs the function a * b
            return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y) 

        elif(f[0] == "avg"):     # performs the function (a + b)/2.0
            return .5 * (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))

        elif(f[0] == "cos_pi"):    #performs the function cos(pi*x)
            return math.cos(math.pi * evaluate_random_function(f[1], x, y))

        elif(f[0] == "sin_pi"):    #performs the function sin(pi*x)
            return math.sin(math.pi * evaluate_random_function(f[1], x, y))           

        elif(f[0] == "square"):    #performs the function x**2
            return evaluate_random_function(f[1], x, y)**2

        elif(f[0] == "absolute_diff"):   #performs the function abs(x)-abs(y)
            return abs(evaluate_random_function(f[1], x, y)) - abs(evaluate_random_function(f[2], x, y))       







def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    

    #takes two ranges and computes their ratio, then use that ratio to find the distance from the lower bound in terms of the remapped interval


    input_range = input_interval_end - input_interval_start 
    output_range = output_interval_end - output_interval_start 

    remap_ratio = float(output_range) / float(input_range)

    newval = output_interval_start + (val - input_interval_start) * remap_ratio

    return newval




def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(9,11)
    green_function = build_random_function(9,11)
    blue_function = build_random_function(9,11)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    

    #Using t to make movies.

    for tbig in range(100):
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        treal = remap_interval(tbig, 0, 100,-1,1)
        fname = "frame{}.png".format(tbig)
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x, y, treal)),
                        color_map(green_function(x, y, treal)),
                        color_map(blue_function(x, y, treal))
                        )

        im.save(fname)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function

    generate_art("myart9.png")

    #print build_random_function(1,5)

    #doctest.run_docstring_examples(evaluate_random_function,globals(),verbose=True)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
