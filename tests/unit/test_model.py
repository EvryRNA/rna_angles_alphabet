"""
Unit test to check if a model is well saved and can be loaded
"""
import os
import unittest

from src.utils import get_angle, labels_to_seq, save_model, load_model

path = os.path.join("tests", "data", "test_unit.txt")


class ModelTest(unittest.TestCase):

    def test_get_angle(self):
        """
        Test the get angle function
        """
        with open(path, 'w') as file_test:
            file_test.write("ETA,THETA\n0,1")
        test_array = get_angle(path, "rna")
        self.assertEqual([0, 1], [test_array[0][0], test_array[0][1]])
        os.remove(path)

    
    def test_labels_to_seq(self):
        """
        Test the labels to seq function
        """
        test_labels = [-1, 0, 1, 3, -1, 2, 3, 0, -1,]
        self.assertEqual("-ABD-CDA-", labels_to_seq(test_labels))


    def test_load_model(self):
        """
        Test if the model is being load properly
        """
        save_model(path, "test")
        model_load = load_model(path)
        self.assertEqual("test", model_load)
        os.remove(path)
        # TODO : INFERENCE APRES FIT
        # model_load = load_model(path)
        # x_test, y_test = [0, 1, 2] , [0, 0, 1]
        # y_pred = model_load.predict(x_test)
        # self.assertEqual(y_pred, y_test)


if __name__ == "__main__":
    unittest.main()
