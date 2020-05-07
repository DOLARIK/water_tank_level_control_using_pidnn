import numpy as np
from scipy.special import expit

class PIDNN:
	"""docstring for PIDNN"""
	def __init__(self, set_point, actual_value, prev_output = 0, learning_rate = 0.01, last_layer_activation_function = 'tanh'):
		super(PIDNN, self).__init__()
		self.set_point = set_point
		self.prev_actual_value = actual_value
		self.prev_output = prev_output
		self.weights = np.ones((3, 1))
		self.learning_rate = learning_rate
		self.prev_error_value = set_point - actual_value
		self.last_layer_activation_function = last_layer_activation_function
		self.__call__(actual_value)

	def __call__(self, actual_value):
		# Forward Propagation
		error_value = self.error(actual_value)
		input_array = self.input_layer(error_value)
		output = self.calculate_output(input_array)

		# Backward Propagation
		grad = self.learning_rate*self.gradient(actual_value, output, error_value, input_array)
		self.weights -= grad

		self.prev_actual_value = actual_value
		self.prev_output = output
		self.prev_error_value = error_value

	def calculate_output(self, input_array):
		if self.last_layer_activation_function == 'sigmoid':
			return expit(np.matmul(input_array, self.weights))[0,0]
		elif self.last_layer_activation_function == 'tanh':
			return np.tanh(np.matmul(input_array, self.weights))[0,0]


	def gradient(self, actual_value, output, error_value, input_layer):
		del_o_del_w = input_layer
		if self.last_layer_activation_function == 'tanh':
			del_u_del_o = (1 - output*output)
		elif self.last_layer_activation_function == 'sigmoid':
			del_u_del_o = output*(1 - output)

		del_y_del_u = self.del_y_del_u(actual_value, output)
		del_e_del_y = -1
		del_J_del_e = self.del_J_del_e(error_value)
		del_J_del_w = del_J_del_e*del_e_del_y*del_y_del_u*del_u_del_o*del_o_del_w.T

		return del_J_del_w

	def del_J_del_e(self, error_value):
		return 0.5*(error_value - self.prev_error_value)

	def del_y_del_u(self, actual_value, output):
		del_y = actual_value - self.prev_actual_value
		del_u = output - self.prev_output
		return np.sign(del_u*del_y)

	def input_layer(self, error_value):
		return np.expand_dims(np.asarray([self.proportional_input(error_value), self.integral_input(error_value), self.derivative_input(error_value)]), axis = 0)

	def error(self, actual_value):
		return self.set_point - actual_value

	def proportional_input(self, error_value):
		if error_value > 1:
			return 1
		elif error_value < -1:
			return -1
		else:
			return error_value

	def integral_input(self, error_value):
		if error_value > 1:
			return 1
		elif error_value < -1:
			return -1
		else:
			return error_value + self.error(self.prev_actual_value)

	def derivative_input(self, error_value):
		if error_value > 1:
			return 1
		elif error_value < -1:
			return -1
		else:
			return error_value - self.error(self.prev_actual_value)