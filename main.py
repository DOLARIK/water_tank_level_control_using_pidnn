from system import System

water_level_setpoint = 1000 # in meters
maximum_flowrate = 10 # in litres per minute

system = System(water_level_setpoint = water_level_setpoint, maximum_flowrate = maximum_flowrate)
system.start_simulation()