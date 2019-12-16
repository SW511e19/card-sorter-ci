class Motor():
    def __init__(self, motor):
        self.motor = motor
    
    def run_to_abs_pos(self, position_sp, speed_sp):
        print("Ran motor " + str(self) +"with position : " + str(position_sp) + " and Speed : " + str(speed_sp))

class LargeMotor(Motor):
    def __init__(self, motor):
        super()

class MediumMotor(Motor):
    def __init__(self, motor):
        super()


