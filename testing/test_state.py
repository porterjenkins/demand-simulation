import unittest

from state import State

class TestBuffer(unittest.TestCase):

    def test_get_num_slots(self):

        example = {
            'deli-cooler': {
                0: ('coca_cola_20oz_bottle', 5),
                1: ('coca_cola_20oz_bottle', 5),
                2: ('coca_cola_20oz_bottle', 5),
                3: ('sprite_20oz_bottle', 5),
                4: ('Monster_16oz_can', 5),
                5: ('Monster_16oz_can', 5)
            },
            'dairy-cooler': {
                0: ('dr_pepper_20oz_bottle', 5),
                1: ('dr_pepper_20oz_bottle', 5),
                2: ('sprite_20oz_bottle', 5),
                3: ('sprite_20oz_bottle', 5),
            }
        }

        gt = {
            'deli-cooler': {
                "coca_cola_20oz_bottle": 3,
                "sprite_20oz_bottle": 1,
                "Monster_16oz_can": 2
            },
            'dairy-cooler': {
                "dr_pepper_20oz_bottle": 2,
                "sprite_20oz_bottle": 2
            }
        }

        output = State.get_sum_slots(example)
        assert gt == output
