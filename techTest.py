import numpy, argparse
#import ipdb; ipdb.set_trace()


class Image(object):
    image = []
    dimensions = []

    def __init__(self, width, height):
        self.dimensions = [width, height]

    def clear_image(self):
        '''
        clears the image- sets all pixel values to 0
        '''
        self.image = numpy.zeros((self.dimensions[0] * self.dimensions[1]), dtype=int).reshape(self.dimensions[0], self.dimensions[1])

    def set_pixel_colour(self, x, y, colour):
        '''
        sets a specific pixel to the value specified in 'colour'
        '''
        self.image[y, x] = colour

    def set_vertical_line_colour(self, x, y1, y2, colour):
        '''
        sets a vertical line to a specific value
        '''
        if y1 == (y2 - 1):
            self.set_pixel_colour(x, y1, colour)
        else:
            self.image[y1:y2, x] = colour

    def set_horizontal_line_colour(self, x1, x2, y, colour):
        '''
        sets a horizontal line to a specific value
        '''
        if x1 == (x2 - 1):
            self.set_pixel_colour(x1, y, colour)
        else:
            self.image[y, x1:x2] = colour

    def remove_duplicates(self, definitive_list, new_list):
        '''
        appends all items in new_list to definitive_list only if they do not already
        exist in definitive_list
        '''
        for item in new_list:
            if item not in definitive_list:
                definitive_list.append(item)
        return definitive_list

    def fill_region(self, x, y, colour):
        '''
        fills an area, the area is any pixel which is connected to the source pixel either
        vertically or horizontally and has the same colour as the source pixel
        '''
        original_colour = self.image[x, y]
        region = [[x, y]]
        recursion_count = 0
        region = self.find_region(region, original_colour, recursion_count)
        for pixel in region:
            self.image[pixel[0], pixel[1]] = colour

    def find_neighbours(self, x, y):
        '''
        finds the pixels to the left, right, up and down of the source pixel
        '''
        neighbours = []
        if x - 1 >= 0:
            neighbours.append([x - 1, y])

        if x + 1 < self.image.shape[0]:
            neighbours.append([x + 1, y])

        if y - 1 >= 0:
            neighbours.append([x, y - 1])

        if y + 1 < self.image.shape[1]:
            neighbours.append([x, y + 1])

        return neighbours

    def check_neighbours(self, neighbours, original_colour):
        '''
        we are only interested in a neighbouring pixel if it has the same colour as the original
        '''
        region = []
        for neighbour in neighbours:
            if self.image[neighbour[0], neighbour[1]] == original_colour:
                region.append(neighbour)

        return region

    def find_region(self, region, original_colour, recursion_count):
        '''
        find all the pixels which share a border and colour
        '''
        if recursion_count < len(region):  # if there are pixels in the region which we've not yet checked
            pixel = region[recursion_count]
            this_pixels_neighbours = self.find_neighbours(pixel[0], pixel[1])
            region = self.remove_duplicates(region, self.check_neighbours(this_pixels_neighbours, original_colour))
            #recursion_count += 1
            self.find_region(region, original_colour, recursion_count+1)

        return region


new_image = None
while True:
    user_input = raw_input('type away: ')
    args = user_input.split()
    try:
        if args[0] == 'I':
            if len(args) > 3:
                raise IndexError
            else:
                new_image = Image(int(args[1]), int(args[2]))
                new_image.clear_image()
        elif args[0] == 'C':
            if len(args) > 1:
                raise IndexError
            else:
                new_image.clear_image()
        elif args[0] == 'L':
            if len(args) > 4:
                raise IndexError
            else:
                new_image.set_pixel_colour(int(args[1]) - 1, int(args[2]) - 1, args[3])  # -1 because the origin is 1,1, not 0,0
        elif args[0] == 'H':
            if len(args) > 5:
                raise IndexError
            else:
                new_image.set_horizontal_line_colour(int(args[1]) - 1, int(args[2]), int(args[3]) - 1, args[4])  # x2 is inclusive, so we don't minus 1
        elif args[0] == 'V':
            if len(args) > 5:
                raise IndexError
            else:
                new_image.set_vertical_line_colour(int(args[1]) - 1, int(args[2]) - 1, int(args[3]), args[4])  # y2 is inclusive, so we don't minus 1
        elif args[0] == 'F':
            if len(args) > 4:
                raise IndexError
            else:
                new_image.fill_region(int(args[1]) - 1, int(args[2]) - 1, args[3])
        elif args[0] == 'S':
            if len(args) > 1:
                raise IndexError
            else:
                print new_image.image
        elif args[0] == 'X':
            if len(args) > 1:
                raise IndexError
            else:
                break
        elif args[0] == 'Help':
            print '''The editor supports 7 commands:

                1.I M N. Create a new M x N image with all pixels coloured white (O).
                2.C. Clears the table, setting all pixels to white (O).
                3.L X Y C. Colours the pixel (X,Y) with colour C.
                4.V X Y1 Y2 C. Draw a vertical segment of colour C in column X between rows Y1 and Y2 (inclusive).
                5.H X1 X2 Y C. Draw a horizontal segment of colour C in row Y between columns X1 and X2 (inclusive).
                6.F X Y C. Fill the region R with the colour C. R is defined as: Pixel (X,Y) belongs to R. Any other
                pixel which is the same colour as (X,Y) and shares a common side with any pixel in R also belongs to this region.
                7.S. Show the contents of the current image
                8.X. Terminate the session'''
        else:
            print 'Unexpected input, type "Help" for allowed parameters'
    except (AttributeError):
        print 'No image found, you must create an image before you can clear it. Type "Help" for a list of commands'
    except (IndexError):
        print 'Wrong number of parameters entered. Type "Help" for a list of commands'
