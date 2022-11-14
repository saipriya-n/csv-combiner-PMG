import sys
import os
import pandas

class CSVCombinerPMG:

    @staticmethod
    def file_paths_validation(user_arguments):     #creating a utility function called file_paths_validation that takes the argument values entered in the command line as its parameters 
                                                   #and returns a boolean value after valding the file_path, size exist or not 
        #checking various consitions for the entered file paths
        if (len(user_arguments) <= 1):
            print("Path Error: No file-paths given in input. Please enter the commad line query correctly: +
                  "python ./csv_combiner.py ./fixtures/household_cleaners.csv ./fixtures/accessories.csv > combined.csv")
            return False
            
        for file_path in user_arguments[1:]: 
            if (os.stat(file_path).st_size == 0): #for each file_path entered it will check the size, if it's zero then it will give a warning that the csv file is empty 
                print("Message: Warning-This is an empty file: " + file_path)
                return False
            if (!os.path.exists(file_path)): #for each file_path entered it will if the path exists are not 
                print("Message: Error-This file or directory cannot be found: " + file_path)
                return False
        return True

    def combine_files_listed(self, user_arguments: list):
        block_list = []
        
        if (self.file_paths_validation(user_arguments)): #consition checks if the path of the enetred argument value is valid or no 
            for file_path in user_arguments[1:]:
                for block in pandas.read_csv(file_path, chunksize=10**6):
                    block['filename'] = os.path.basename(file_path) #retrieving the fileName from basepath of the file
                    block_list.append(block) #adds the fileName column to the block
           
            for file_chunk in block_list:
                print(file_chunk.to_csv(index=False, line_terminator='\n', chunksize=10**6, header=True,), end='')
        else:
            return

def main():
    PMGCSVCombiner = CSVCombinerPMG() #creating a class object
    PMGCSVCombiner.combine_files_listed(sys.argv) #calling the combine_files_listed function of CSVCombinerPMG class and passing the parameter that takes all argument values entered in the command line 


if __name__ == '__main__':
    main()