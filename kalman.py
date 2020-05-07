import numpy as np

class Kalman:

    def __init__(self, initial_state, initial_error_covariance_matrix,
                        transition_matrix, process_noise,
                        input_matrix, input_vector,
                        measurement_matrix, measurement_noise):

        self.initial_state = initial_state
        self.initial_error_covariance_matrix = initial_error_covariance_matrix

        self.transition_matrix = transition_matrix
        self.process_noise = process_noise

        self.input_matrix = input_matrix
        self.input_vector = input_vector

        self.measurement_matrix = measurement_matrix
        self.measurement_noise = measurement_noise

        self.prioris = []
        self.error_covariance = initial_error_covariance_matrix

        self.posterioris = []
        self.posterioris.append(initial_state)

    def __call__(self, sensor_readings, input_vector = None):

        if input_vector is None:
            input_vector = self.input_vector

        # PRIORI CALCULATION, PRIORI_ERROR_COVARIANCE
        priori, predicted_error_covariance = self.state_prediction(
                                                        state_vector = self.posterioris[-1],
                                                        input_vector = input_vector,
                                                        error_covariance = self.error_covariance)

        self.prioris.append(priori)

        # OBSERVE READINGS, EXPECTED_READINGS, EXPECTED_ERROR_COVARIANCE
        expected_readings, expected_error_covariance = self.expectations(priori = priori,
                                                                    predicted_error_covariance = predicted_error_covariance)


        # KALMAN_GAIN
        kalman_gain_matrix = self.kalman_gain(predicted_error_covariance, expected_error_covariance)

        # POSTERIORI CALCULATION
        posteriori = self.state_update(
                        sensor_readings = sensor_readings,
                        kalman_gain_matrix = kalman_gain_matrix,
                        expected_readings = expected_readings,
                        predicted_error_covariance = predicted_error_covariance)


        self.posterioris.append(posteriori)

        return np.reshape(priori, self.initial_state.shape), np.reshape(posteriori, self.initial_state.shape)

    # PRIORI CALCULATION, PRIORI_ERROR_COVARIANCE
    def priori_calculation(self, state_vector, input_vector = None):
        if input_vector is None:
            input_vector = self.input_vector
        return  np.matmul(self.transition_matrix, state_vector.reshape(state_vector.size, 1)) + self.input_matrix.reshape(state_vector.size, input_vector.shape[0])*input_vector

    def priori_error_covariance_calculation(self, error_covariance):
        return np.matmul(np.matmul(self.transition_matrix, error_covariance), self.transition_matrix.T) + self.process_noise

    def state_prediction(self, state_vector, input_vector, error_covariance):

        priori = self.priori_calculation(state_vector, input_vector)
        priori_error_covariance = self.priori_error_covariance_calculation(error_covariance)

        return priori, priori_error_covariance


    # OBSERVE READINGS, EXPECTED_READINGS, EXPECTED_ERROR_COVARIANCE
    def expected_readings_calculation(self, priori):
        return np.matmul(self.measurement_matrix, priori)

    def expected_error_covariance_calculation(self, predicted_error_covariance):
        return np.matmul(np.matmul(self.measurement_matrix, predicted_error_covariance), self.measurement_matrix.T)

    def expectations(self, priori, predicted_error_covariance):

        expected_readings = self.expected_readings_calculation(priori)
        expected_error_covariance = self.expected_error_covariance_calculation(predicted_error_covariance)

        return expected_readings, expected_error_covariance


    # KALMAN_GAIN
    def kalman_gain(self, predicted_error_covariance, expected_error_covariance):
        return np.matmul(np.matmul(predicted_error_covariance, self.measurement_matrix.T), np.linalg.inv(expected_error_covariance + self.measurement_noise))


    # POSTERIORI CALCULATION
    def posteriori_calculation(self, sensor_readings, kalman_gain_matrix, expected_readings):
        return self.prioris[-1] + np.matmul(kalman_gain_matrix, (sensor_readings.reshape(sensor_readings.size, 1) - expected_readings))

    def posteriori_error_covariance_calculation(self, kalman_gain_matrix, predicted_error_covariance):
        return predicted_error_covariance - np.matmul(kalman_gain_matrix, np.matmul(self.measurement_matrix, predicted_error_covariance))

    def state_update(self, sensor_readings, kalman_gain_matrix,
                                    expected_readings, predicted_error_covariance):

        posteriori = self.posteriori_calculation(sensor_readings, kalman_gain_matrix, expected_readings)
        updated_error_covariance = self.posteriori_error_covariance_calculation(kalman_gain_matrix, predicted_error_covariance)

        self.error_covariance = updated_error_covariance

        return posteriori
