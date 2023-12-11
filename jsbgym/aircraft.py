import collections


class Aircraft(
    collections.namedtuple(
        "Aircraft", ["jsbsim_id", "flightgear_id", "name", "cruise_speed_kts"]
    )
):
    KTS_TO_M_PER_S = 0.51444
    KTS_TO_FT_PER_S = 1.6878

    def get_max_distance_m(self, episode_time_s: float) -> float:
        """Estimates the maximum distance this aircraft can travel in an episode"""
        margin = 0.1
        return (
            self.cruise_speed_kts * self.KTS_TO_M_PER_S * episode_time_s * (1 + margin)
        )

    def get_cruise_speed_fps(self) -> float:
        return self.cruise_speed_kts * self.KTS_TO_FT_PER_S


c172 = Aircraft("c172p", "c172p", "C172", 120)
pa28 = Aircraft("pa28", "PA28-161-180", "PA28", 130)
j3 = Aircraft("J3Cub", "J3Cub", "J3", 70)
f15 = Aircraft("f15", "f15c", "F15", 500)
f16 = Aircraft("f16", "f16-block-52", "F16", 550)
ov10 = Aircraft("OV10", "OV10_USAFE", "OV10", 200)
pc7 = Aircraft("pc7", "pc7", "PC7", 170)
a320 = Aircraft("A320", "A320-200-CFM", "A320", 250)
b747 = Aircraft("B747", "747-400", "B747", 250)
md11 = Aircraft("MD11", "MD-11", "MD11", 250)
dhc6 = Aircraft("DHC6", "dhc6jsb", "DHC6", 170)
