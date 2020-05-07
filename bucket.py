
class Bucket:
	"""docstring for Bucket"""
	def __init__(self, radius, initial_water_amount = 0):
		super(Bucket, self).__init__()
		self.radius = radius
		self.water_amount = initial_water_amount
		self.water_level = 0
		self.update_water_level()

	def update_state(self, flowrate, time_interval):
		water_amount = self.calculate_water_amount_based_on_flowrate(flowrate, time_interval)
		self.update_water_amount(water_amount)
		self.update_water_level()

	def water_height(self, water_amount):
		return water_amount/(3.14*self.radius*self.radius)

	def update_water_amount(self, water_amount):
		self.water_amount += water_amount
		self.water_amount = max(0, self.water_amount)

	def update_water_level(self):
		self.water_level = self.water_height(self.water_amount)

	def calculate_water_amount_based_on_flowrate(self, flowrate, time_interval):
		return flowrate*time_interval