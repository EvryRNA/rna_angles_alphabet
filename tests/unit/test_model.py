"""
Unit test to check if a model is well saved and can be loaded
"""
import os
import unittest


from src.utils import get_angle, text_to_csv, save_model, load_model

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
            text_to_csv(path)
        self.assertTrue(os.path.isfile(f"{path[:-4]}.csv"))
        os.remove(path)
        os.remove(f"{path[:-4]}.csv")
        

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




if __name__ == "__main__":
    unittest.main()
