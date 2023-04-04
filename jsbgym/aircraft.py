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


cessna172P = Aircraft("c172p", "c172p", "Cessna172P", 120)
pa28 = Aircraft("pa28", "PA28-161-180", "PA28", 130)
f15 = Aircraft("f15", "f15c", "F15", 500)
f16 = Aircraft("f16", "f16-block-52", "F16", 550)
a320 = Aircraft("A320", "A320-200-CFM", "A320", 480)
b747 = Aircraft("B747", "787-400", "B747", 490)
