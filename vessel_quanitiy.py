class Vessel:
    def __init__(self, SDWT, density=0.85, non_cargo_percentage=0.06, block_coefficient=0.85, beam=50, length=300):
        """
        Initialize the Vessel object with given parameters.
        
        :param SDWT: Summer Deadweight in metric tons
        :param density: Density of crude oil in metric tons per cubic meter (default is 0.85)
        :param non_cargo_percentage: Percentage of SDWT that accounts for non-cargo weights (default is 6%)
        :param block_coefficient: Block coefficient (default is 0.85 for large tankers)
        :param beam: Beam (width) of the vessel in meters (default is 50 meters)
        :param length: Length of the vessel in meters (default is 300 meters)
        """
        self.SDWT = SDWT
        self.density = density
        self.non_cargo_percentage = non_cargo_percentage
        self.block_coefficient = block_coefficient
        self.beam = beam
        self.length = length
        self.cubic_meter_to_barrel = 6.2898
        self.non_cargo_weights = self.SDWT * self.non_cargo_percentage
        self.available_cargo_weight = self.SDWT - self.non_cargo_weights
    
    def calculate_max_capacity(self):
        """
        Calculate the maximum crude oil capacity in barrels if draught is not provided.
        
        :return: Maximum crude oil capacity in barrels
        """
        cargo_volume_m3 = self.available_cargo_weight / self.density
        cargo_volume_bbl = cargo_volume_m3 * self.cubic_meter_to_barrel
        return cargo_volume_bbl
    
    def calculate_with_draught(self, draught):
        """
        Calculate the current crude oil on board and the remaining capacity in barrels based on the provided draught.
        
        :param draught: Draught in meters
        :return: Tuple containing maximum crude oil capacity, current crude oil on board, and remaining capacity in barrels
        """
        # Calculate the displacement volume based on draught
        displacement_volume = self.length * self.beam * draught * self.block_coefficient
        
        # Convert the displacement volume to crude oil volume in barrels
        current_crude_oil_bbl = displacement_volume * self.cubic_meter_to_barrel
        
        # Calculate the maximum cargo volume in barrels
        max_cargo_volume_m3 = self.available_cargo_weight / self.density
        max_cargo_volume_bbl = max_cargo_volume_m3 * self.cubic_meter_to_barrel
        
        # Calculate the remaining capacity in barrels
        remaining_capacity_bbl = max_cargo_volume_bbl - current_crude_oil_bbl
        
        return max_cargo_volume_bbl, current_crude_oil_bbl, remaining_capacity_bbl


# Example usage:
SDWT = 299011  # Example Summer Deadweight in metric tons

# Create a Vessel object
vessel = Vessel(SDWT)

# Calculate crude oil capacity without draught
max_capacity_bbl = vessel.calculate_max_capacity()
print(f"Maximum crude oil capacity: {max_capacity_bbl:.2f} bbl")

# Calculate current crude oil and remaining capacity with draught
draught = 15  # Example draught in meters
max_capacity_bbl, current_crude_oil_bbl, remaining_capacity_bbl = vessel.calculate_with_draught(draught)
print(f"Maximum crude oil capacity: {max_capacity_bbl:.2f} bbl")
print(f"Current crude oil on board: {current_crude_oil_bbl:.2f} bbl")
print(f"Remaining capacity: {remaining_capacity_bbl:.2f} bbl")
