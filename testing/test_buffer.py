import unittest

from sim.buffer import Buffer

class TestBuffer(unittest.TestCase):

    """def setupClass(cls):
        cls.buffer = Buffer()"""

    def test_get_sum_reward(self):
        buffer = Buffer()

        example = [
            {
                'entrance-cooler':
                    {
                        'diet_coke_20oz_bottle':
                        {
                            'total_sales': 1.99,
                            'q_sold': 1,
                            'region': 'entrance'
                        },
                        'coca_cola_20oz_bottle':
                      {
                          'total_sales': 3.98,
                          'q_sold': 2,
                          'region': 'entrance'
                      }
                  }
             },
            {
                'entrance-cooler':
                    {
                        'diet_coke_20oz_bottle':
                            {
                                'total_sales': 1.99,
                                'q_sold': 1,
                                'region': 'entrance'
                            },
                        'coca_cola_20oz_bottle':
                            {
                                'total_sales': 3.98,
                                'q_sold': 2,
                                'region': 'entrance'
                            }
                    }
            },
        ]
        gt = {
                'entrance-cooler':
                    {
                        'diet_coke_20oz_bottle':
                        {
                            'total_sales': 3.98,
                            'q_sold': 2,
                            'region': 'entrance'
                        },
                  'coca_cola_20oz_bottle':
                      {
                          'total_sales': 7.96,
                          'q_sold': 4,
                          'region': 'entrance'
                      }
                  }
             }

        output = buffer.get_sum_rewards(example)
        assert output == gt


    def test_get_num_slots(self):

        buffer = Buffer()

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

        output = buffer.get_sum_slots(example)
        assert gt == output