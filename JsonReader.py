import json  # for reading json files
import warnings # for filtering warning

warnings.filterwarnings('ignore')


class FileNotFoundException(Exception):
    """Raised when the file path which is passed in the variable is invalid"""
    pass


class ContentNotFound(Exception):
    """Raised when trying to fetch a content fron the json file which is not present in the file"""
    def __init__(self, string, message="Content Not found in the given json file"):
        self.string = string  # returns the string
        self.message = message  # Return the error message
        super().__init__(self.message+f". Try correcting spelling of '{string}'")
    

class JsonReader:
    """
    Parent Reader class that will open all the files as provided in the constant variable in the file
    all remaining classes will inherit this class for the data from the json files
    """
    def __init__(self):
        try:
            with open(YOGA_FILE, 'r') as yoga:
                self.yoga_jf = json.load(yoga)
            
        except FileNotFoundException as e:
            print(f"The file {YOGA_FILE} was not found. Please recheck the directory", e)

        try:
            with open(DIET_FILE, 'r') as diet:
                self.diet_jf = json.load(diet)
            
        except FileNotFoundException as e:
            print(f"The file {YOGA_FILE} was not found. Please recheck the directory", e)
    

class Yoga(JsonReader):

    def get_all_asans(self):
        """This Function Returns a list of asans present in the yoga.json file

        Returns:
            list: this list contains all the keys for Asans present in the Yoga.json File
        """
        data = []
        for i in self.yoga_jf['Yoga']:
            data.append(str(i).lower()) 
        return data
    def get_asan_data(self, string):
        self.asans = self.get_all_asans()
        for i,j in enumerate(self.asans, start=0):
            if j == str(string).lower():
                return self.yoga_jf['Yoga'][str(self.asans[i]).title()] 
            else: 
                raise ContentNotFound(string)
                
    def get_asan_content(self, string, *arguments):
        """perform a quick search and returns a list of all the contents of the asan specified in the string variable

        Args:
            string (str): Asan Name

        Returns:
            List: return a list with [Asan_Name, *args()]
        """
        asan_info = self.get_asan_data(string)
        ret_data = []
        ret_data.append(string)
        for i,x in enumerate(asan_info, start=0):
            args = list(arguments)
            if x in args:
                ret_data.append(self.yoga_jf['Yoga'][str(self.asans[i]).title()][x])
            else:
                pass
        return ret_data



YOGA_FILE = './static/json/yoga.json'
DIET_FILE = './static/json/diet.json'

jr = Yoga()
print(jr.get_asan_content("Kapal Bhati", "sub_desc", "img_id", "desc"))