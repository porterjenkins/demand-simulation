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

