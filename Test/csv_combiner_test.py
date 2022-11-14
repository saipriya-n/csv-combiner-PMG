import sys
import os
import pandas
from io import StringIO
import unittest
import test_generatefixtures
from csv_combiner import CSVCombinerPMG

class TestCombineMethod(unittest.TestCase):
    
    test_output_path = "./test_output.csv"
    test_output = open(test_output_path, 'w+')
    csv_combiner_path = "./csv_combiner.py"
    accessories_path = "./test_fixtures/accessories.csv"
    clothing_path = "./test_fixtures/clothing.csv"
    household_cleaners_path = "./test_fixtures/household_cleaners.csv"
    empty_file_path = "./test_fixtures/empty_file.csv"
    file_backUp = sys.stdout
    PMGCSVCombiner = CSVCombinerPMG()

    @classmethod
    def setUpClass(cls):
        test_generatefixtures.main() #creating generatefixtures files
        sys.stdout = cls.test_output 

    @classmethod
    def tearDownClass(cls):

        cls.test_output.close()
        if os.path.exists(cls.test_output_path):
            os.remove(cls.test_output_path)
        if os.path.exists(cls.accessories_path):
            os.remove(cls.accessories_path)
        if os.path.exists(cls.clothing_path):
            os.remove(cls.clothing_path)
        if os.path.exists(cls.household_cleaners_path):
            os.remove(cls.household_cleaners_path)
        if os.path.exists(cls.empty_file_path):
            os.remove(cls.empty_file_path)
        if os.path.exists("./test_fixtures"):
            os.rmdir("./test_fixtures")

    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.test_output_path, 'w+')

    def tearDown(self):
        self.test_output.close()
        self.test_output = open(self.test_output_path, 'w+')
        sys.stdout = self.file_backUp
        self.test_output.truncate(0)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

    #testing correct test cases
    def test_filename_row_and_column_isAdded(self): #checking if the fileName column and its value has been addeed or no
        user_arguments = [self.csv_combiner_path, self.accessories_path, self.clothing_path]
        self.PMGCSVCombiner.combine_files_listed(user_arguments)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        with open(self.test_output_path) as f:
            data_frame = pandas.read_csv(f)
        self.assertIn('filename', data_frame.columns.values)

        with open(self.test_output_path) as f:
            data_frame = pandas.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertIn('accessories.csv', data_frame['filename'].tolist())

    def test_values_in_combined(self): #checking if values for all files are present in the newly created output file 
        user_arguments = [self.csv_combiner_path, self.accessories_path, self.clothing_path,
                self.household_cleaners_path]
        self.PMGCSVCombiner.combine_files_listed(user_arguments)
        self.test_output.write(self.output.getvalue())
        self.test_output.close()
        accessories_data_frame = pandas.read_csv(filepath_or_buffer=self.accessories_path, lineterminator='\n')
        clothing_data_frame = pandas.read_csv(filepath_or_buffer=self.clothing_path, lineterminator='\n')
        household_cleaners_data_frame = pandas.read_csv(filepath_or_buffer=self.household_cleaners_path, lineterminator='\n')

        with open(self.test_output_path) as f:
            files_combined_data_frame = pandas.read_csv(filepath_or_buffer=f, lineterminator='\n')
        self.assertEqual(len(files_combined_data_frame.merge(accessories_data_frame)), len(files_combined_data_frame.drop_duplicates()))
        self.assertEqual(len(files_combined_data_frame.merge(clothing_data_frame)), len(files_combined_data_frame.drop_duplicates()))
        self.assertEqual(len(files_combined_data_frame.merge(household_cleaners_data_frame)), len(files_combined_data_frame.drop_duplicates()))
    
    #testing for incorrect test cases
    def test_no_file_paths(self): #running class with no arguments
        user_arguments = [self.csv_combiner_path] 
        self.PMGCSVCombiner.combine_files_listed(user_arguments)
        self.assertIn("Error: No file-paths input.", self.output.getvalue())

    def test_files_that_are_empty(self):#testing for an empty file
        user_arguments = [self.csv_combiner_path, self.empty_file_path]
        self.PMGCSVCombiner.combine_files_listed(user_arguments)
        self.assertIn("Warning: The following file is empty: ", self.output.getvalue())

    def test_files_that_do_not_exist(self): #testing for file that does not exist
        user_arguments = [self.csv_combiner_path, "do_not_exist.csv"]
        self.PMGCSVCombiner.combine_files_listed(user_arguments)
        self.assertTrue("Error: File or directory not found:" in self.output.getvalue())



