import file_analyzer
import unittest

# For testing I created fake_dictionary with several types of files. I aslo wanted to use pyfakers to mock the file system, but I did not have enough time for this. Also I could have added more types of files and tests for exceptions or other unexpected situations.

class Test(unittest.TestCase):    
    def test_without_parameters(self):
        print("Result of file_analyzer.analyze_file(directory = 'fake_directory', threshold = None, is_recursive = False)")
        categories = {}
        categories['directory'] = [['fake_directory/folder1', 'fake_directory/folder2'], 8192]
        large_files = []
        unusual_permission_files = ['fake_directory/folder1', 'fake_directory/folder2'] # both have permissions drwxrwxrwx

        received_categories, received_large_files, received_unusual_permission_files = file_analyzer.analyze_file(directory = 'fake_directory', threshold = None, is_recursive = False)

        print("\n\n")

        self.assertEqual(categories, received_categories)
        self.assertEqual(large_files, received_large_files)
        self.assertEqual(unusual_permission_files, received_unusual_permission_files)

    def test_recursive(self):
        print("Result of file_analyzer.analyze_file(directory = 'fake_directory', threshold = None, is_recursive = True)")
        categories = {}
        categories['text/plain'] = [['fake_directory/folder1/aba.txt', 'fake_directory/folder1/abacaba'], 13]
        categories['image/png'] = [['fake_directory/folder1/PeterM_Flower.png'], 36559]
        categories['directory'] = [['fake_directory/folder1', 'fake_directory/folder2'], 8192]
        categories['text/x-shellscript'] = [['fake_directory/folder2/exec.sh'], 32]
        large_files = []
        unusual_permission_files = ['fake_directory/folder1/PeterM_Flower.png', 'fake_directory/folder1', 'fake_directory/folder2/exec.sh', 'fake_directory/folder2']

        received_categories, received_large_files, received_unusual_permission_files = file_analyzer.analyze_file(directory = 'fake_directory', threshold = None, is_recursive = True)

        print("\n\n")

        self.assertEqual(categories, received_categories)
        self.assertEqual(large_files, received_large_files)
        self.assertEqual(unusual_permission_files, received_unusual_permission_files)

    def test_recursive_with_threshold(self):
        print("Result of file_analyzer.analyze_file(directory = 'fake_directory', threshold = 9000, is_recursive = True)")
        categories = {}
        categories['text/plain'] = [['fake_directory/folder1/aba.txt', 'fake_directory/folder1/abacaba'], 13]
        categories['image/png'] = [['fake_directory/folder1/PeterM_Flower.png'], 36559]
        categories['directory'] = [['fake_directory/folder1', 'fake_directory/folder2'], 8192]
        categories['text/x-shellscript'] = [['fake_directory/folder2/exec.sh'], 32]
        large_files = [('fake_directory/folder1/PeterM_Flower.png', 36559)]
        unusual_permission_files = ['fake_directory/folder1/PeterM_Flower.png', 'fake_directory/folder1', 'fake_directory/folder2/exec.sh', 'fake_directory/folder2']

        received_categories, received_large_files, received_unusual_permission_files = file_analyzer.analyze_file(directory = 'fake_directory', threshold = 9000, is_recursive = True)

        print("\n\n")

        self.assertEqual(categories, received_categories)
        self.assertEqual(large_files, received_large_files)
        self.assertEqual(unusual_permission_files, received_unusual_permission_files)
        

if __name__ == '__main__':
    unittest.main()

