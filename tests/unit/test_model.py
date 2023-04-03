"""
Unit test to check if a model is well saved and can be loaded
"""
import os
import unittest

from src.plot_helper import get_colors
from src.utils import get_angle, text_to_csv, labels_to_seq, save_model, load_model

path = os.path.join("tests", "data", "test_unit.txt")


class ModelTest(unittest.TestCase):

    def test_get_angle(self):
        """
        Test the get angle function
        """
        with open(path, 'w') as file_test:
            file_test.write("ETA,THETA\n0,1")
        test_array = get_angle(path)
        self.assertEqual([0, 1], [test_array[0][0], test_array[0][1]])
        os.remove(path)
    
    
    def test_text_to_csv(self):
        """
        Test the csv function
        """
        with open(path, 'w') as file_test:
            text_to_csv(path, ["ETA", "THETA"])
        self.assertTrue(os.path.isfile(f"{path[:-4]}.csv"))
        os.remove(path)
        os.remove(f"{path[:-4]}.csv")

    
    def test_labels_to_seq(self):
        """
        Test the labels to seq function
        """
        test_labels = [-1, 0, 1, 2, 3, 7, 1, 0, -1, 3, -1]
        self.assertEqual("-ABCDHBA-D-", labels_to_seq(test_labels))
        

    def test_save_model(self):
        """
        Test the save model function
        """
        save_model(path, None)
        self.assertTrue(os.path.isfile(path))
        os.remove(path)


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


    def test_get_colors(self):
        """
        Test if the function return a list of colors
        """
        list_colors = get_colors(5)
        self.assertTrue(list_colors[0] == "k" and len(list_colors) == 5)

if __name__ == "__main__":
    unittest.main()
