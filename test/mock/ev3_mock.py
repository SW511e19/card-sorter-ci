class Motor():
    def __init__(self, motor):
        position = 0
        self.motor = motor
    
    def run_to_abs_pos(self, position_sp, speed_sp):
        self.position = position_sp
        print("Ran motor " + str(self) +"with position : " + str(position_sp) + " and Speed : " + str(speed_sp))

    def SpeedPercent(self, speed):
        print("Set EV3 Speed on : " + str(self) + str(speed))

class ColorSensor():
    def __init__(self):
        pass

    def MODE_COL_COLOR(self):
        print("SET COLOR MODE")
        return 

    def COLOR_NOCOLOR(self):
        return 0   

    def COLOR_BLACK(self):
        return 1

    def COLOR_BLUE(self):
        return 2

    def COLOR_GREEN(self):
        return 3   

    def COLOR_YELLOW(self):
        return 4

    def COLOR_RED(self):
        return 5

    def COLOR_WHITE(self):
        return 6

    def COLOR_BROWN(self):
        return 7

    def color(self, colorNumber):
        return colorNumber

class LargeMotor(Motor):
    def __init__(self, motor):
        super()

class MediumMotor(Motor):
    def __init__(self, motor):
        super()

