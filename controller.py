import numpy as np
from pidnn import PIDNN
from kalman import Kalman
from process_dynamics import initial_error_covariance_matrix, transition_matrix, input_matrix, input_vector, measurement_matrix, disturbance, uncertainty

class Controller:
	def __init__(self, set_point, water_level, maximum_flowrate, initial_flowrate = 0, learning_rate = 0.1, last_layer_activation_function = 'tanh',
		initial_error_covariance_matrix = initial_error_covariance_matrix, transition_matrix = transition_matrix, 
		input_matrix = input_matrix, input_vector = input_vector, 
		measurement_matrix = measurement_matrix, disturbance = disturbance, uncertainty = uncertainty):

		initial_state = np.asarray([initial_flowrate]).T
		self.kalman = Kalman(initial_state = initial_state, initial_error_covariance_matrix = initial_error_covariance_matrix,
		    transition_matrix = transition_matrix, measurement_matrix = measurement_matrix, input_matrix = input_matrix, input_vector = input_vector, measurement_noise = uncertainty,
		    process_noise = disturbance)

		self.pidnn = PIDNN(set_point = set_point, actual_value = water_level, prev_output = initial_flowrate, learning_rate = learning_rate, last_layer_activation_function = last_layer_activation_function)


		self.maximum_flowrate = maximum_flowrate

	def __call__(self, water_level):
		self.pidnn(actual_value = water_level)
		flowrate = self.pidnn.prev_output*self.maximum_flowrate
		smooth_flowrate = self.kalman(np.asarray([flowrate]))
		smooth_flowrate = smooth_flowrate[1][0]
		return smooth_flowrate


