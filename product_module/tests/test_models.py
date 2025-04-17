import unittest
from product_module.models import YourModel

class TestYourModel(unittest.TestCase):
    def test_model_creation(self):
        model_instance = YourModel(field1='value1', field2='value2')
        self.assertEqual(model_instance.field1, 'value1')
        self.assertEqual(model_instance.field2, 'value2')

if __name__ == '__main__':
    unittest.main()