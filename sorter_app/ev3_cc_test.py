import sys
sys.path.append("test/mock")
import ev3_mock as ev3 # Simulated Test Environment
colorsensor = ev3.ColorSensor()
colorsensor.MODE_COL_COLOR
print("OK")