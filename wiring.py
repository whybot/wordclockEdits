import ast

class wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, config):

        # LED strip configuration:
        language=config.get('stancil_parameter', 'language')
        stancil_content  = ast.literal_eval(config.get('language_options', language))
        self.WCA_HEIGHT  = len(stancil_content)
        self.WCA_WIDTH   = len(stancil_content[0].decode('utf-8'))
        self.LED_COUNT   = self.WCA_WIDTH*self.WCA_HEIGHT # Number of LED pixels.
        self.LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
        self.LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)
        print('Wiring configuration')
        print('  WCA_WIDTH: ' + str(self.WCA_WIDTH))
        print('  WCA_HEIGHT: ' + str(self.WCA_HEIGHT))
        print('  Num of LEDs: ' + str(self.LED_COUNT))

        wiring_layout = config.get('wordclock_display', 'wiring_layout')
        self.wcl = french_wiring(self.WCA_WIDTH, self.WCA_HEIGHT)
        
    def setColorBy1DCoordinates(self, strip, ledCoordinates, color):
        '''
        Linear mapping from top-left to bottom right
        '''
        for i in ledCoordinates:
            self.setColorBy2DCoordinates(strip, i%self.WCA_WIDTH, i/self.WCA_WIDTH, color)

    def setColorBy2DCoordinates(self, strip, x, y, color):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        strip.setPixelColor(self.wcl.getStripIndexFrom2D(x,y), color)
    def getStripIndexFrom2D(self, x,y):
        return self.wcl.getStripIndexFrom2D(x,y)

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        '''
        return self.wcl.mapMinutes(min)

class french_wiring:
    '''
    A class, holding all information of the wordclock's layout to map given
    timestamps, 2d-coordinates to the corresponding LEDs (corresponding to
    the individual wiring/layout of any wordclock).
    If a different wordclock wiring/layout is chosen, this class needs to be
    adopted.
    '''

    def __init__(self, WCA_WIDTH, WCA_HEIGHT):
        self.WCA_WIDTH   = WCA_WIDTH
        self.WCA_HEIGHT  = WCA_HEIGHT
        
        self.WCA_GRID = [[0 for x in range(WCA_HEIGHT+1)] for x in range(self.WCA_WIDTH+1)] 
        self.WCA_GRID[0]=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.WCA_GRID[1]=[21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
        self.WCA_GRID[2]=[22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
        self.WCA_GRID[3]=[43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33]
        self.WCA_GRID[4]=[44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
        self.WCA_GRID[5]=[65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 55]
        self.WCA_GRID[6]=[66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76]
        self.WCA_GRID[7]=[87, 86, 85, 84, 83, 82, 81, 80, 79, 78, 77]
        self.WCA_GRID[8]=[88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98]
        self.WCA_GRID[9]=[109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99]
        #self.WCA_GRID[10]=[110, 88, 87, 66, 65, 44, 43, 22, 21, 0]


    def getStripIndexFrom2D(self, x, y):
        '''
        Mapping coordinates to the wordclocks display
        Needs hardware/wiring dependent implementation
        Final range:
             (0,0): top-left
             (self.WCA_WIDTH-1, self.WCA_HEIGHT-1): bottom-right
        '''
        return self.WCA_GRID[y][x]

    def mapMinutes(self, min):
        '''
        Access minutes (1,2,3,4)
        Needs hardware/wiring dependent implementation
        This implementation assumes the minutes to be wired as first and last two leds of the led-strip
        '''
        
        if min == 1:
            return self.getStripIndexFrom2D(0, 10)
        elif min == 2:
            return self.getStripIndexFrom2D(1, 10)
        elif min == 3:
            return self.getStripIndexFrom2D(8, 10)
        elif min == 4:
            return self.getStripIndexFrom2D(9, 10)
        else:
            print('WARNING: Out of range, when mapping minutes...')
            print(min)
            return self.getStripIndexFrom2D(0, 10)
