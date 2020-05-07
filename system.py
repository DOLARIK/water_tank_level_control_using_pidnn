from bucket import Bucket
from controller import Controller
import numpy as np
import matplotlib.pyplot as plt


class System:

	def __init__(self, water_level_setpoint, time_interval = 0.1, maximum_flowrate = 10, initial_water_amount = 0, radius = 15):
		'''
		maximum_flowrate in litre/minute
		time_interval in seconds
		radius and water_level_setpoint are in cm

		'''
		self.bucket = Bucket(radius = self.cm_to_m(radius), initial_water_amount = initial_water_amount)
		self.controller = Controller(set_point = self.cm_to_m(water_level_setpoint), water_level= self.bucket.water_level, maximum_flowrate = self.lpm_to_m3ps(maximum_flowrate))
		self.time_interval = time_interval
	
	def start_simulation(self, duration = 10, halt_point = .999):
		'''
		duration in minutes
		'''
		duration_in_seconds = self.minutes_to_seconds(duration)

		flowrates = []
		water_levels = []
		time_steps = []
		flowrate_setpoints = []
		water_level_setpoints = []

		step = 0
		pass_1 = False

		while True:
			flowrate = self.controller(self.bucket.water_level)
			self.bucket.update_state(flowrate, self.time_interval)
			print('Time (s): ', step,'Water Level (m): ', self.m_to_cm(self.bucket.water_level), 'Flowrate (l/m): ', self.m3ps_to_lpm(flowrate))

			flowrates.append(self.m3ps_to_lpm(flowrate))
			flowrate_setpoints.append(self.m3ps_to_lpm(self.controller.maximum_flowrate))
			water_levels.append(self.m_to_cm(self.bucket.water_level))
			water_level_setpoints.append(self.m_to_cm(self.controller.pidnn.set_point))
			time_steps.append(step/60)
			
			step += self.time_interval

			if self.bucket.water_level > halt_point*(self.controller.pidnn.set_point) and not pass_1:
				self.controller.pidnn.set_point /= 2 
				# break
				pass_1 = True

			if self.bucket.water_level < (2 - halt_point)*(self.controller.pidnn.set_point) and pass_1:
				break	

		plt.subplot(211)
		plt.plot(time_steps, flowrates)
		plt.plot(time_steps, flowrate_setpoints, 'red')
		plt.plot(time_steps, -np.asarray(flowrate_setpoints), 'red')
		plt.ylabel('flowrate (lpm) \n maximum flowrate = {:.1f} lpm'.format(self.m3ps_to_lpm(self.controller.maximum_flowrate)))
		plt.subplot(212)
		plt.plot(time_steps, water_levels)
		plt.plot(time_steps, water_level_setpoints, 'red')
		plt.ylabel('water level (cm) \n setpoint = {} cm'.format(self.m_to_cm(self.controller.pidnn.set_point)))
		plt.xlabel('time (minutes)')
		plt.show()


		return self.bucket, self.controller

	def lpm_to_m3ps(self, flowrate):
		return flowrate/60000

	def m3ps_to_lpm(self, flowrate):
		return flowrate*60000

	def minutes_to_seconds(self, time):
		return time*60

	def cm_to_m(self, length):
		return length/100

	def m_to_cm(self, length):
		return length*100


if __name__ == '__main__':
	system = System(water_level_setpoint = 1000, maximum_flowrate = 20)
	system.start_simulation()



