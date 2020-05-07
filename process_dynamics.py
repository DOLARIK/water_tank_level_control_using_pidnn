import numpy as np

initial_error_covariance_matrix = 0*np.eye(1)

# dt = 0.02

transition_matrix = np.asarray([[1]])

input_matrix = np.zeros(1).T
input_vector = np.zeros((1,1))

measurement_matrix = np.asarray([[1]])

disturbance = .01*np.eye(1)

uncertainty = 100*np.eye(1)
