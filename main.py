from argparse import ArgumentParser
from sys import stdout

""" provides a class which replaces words in a file"""


class ReplaceString:
    """
        This class replaces a word by another word in a file.
        It works using cli.


        Example
            python3 main.py [--file_name='filename.extenstion'] [--old_word='old word'] [--new_word='new word']  p--replacement_count=[1,2,3....]]

            The [--replacement_count] argument is optional. When not provided, the word is changed througout the whole file
    """

    # The constructor of the class. It initializes the 'file_is_binary' and 'new_file_content' variables
    def __init__(self):
        self.file_is_binary = False
        self.new_file_content = ""

    # the main method. It takes and parses the command line arguments and passes it to the function which does the replacement
    def main(self):
        parser = ArgumentParser()  # create an object of the 'Argument Parser Class'
        # add arguments to the parser
        parser.add_argument('--file_name', type=str, default='', help="Name of target file")
        parser.add_argument('--old_word', type=str, default='', help="The word you want to replace")
        parser.add_argument('--new_word', type=str, default='', help="The new word")
        parser.add_argument('--replacement_count', type=int, default=-1, help="Number of words you want to replace")

        args = parser.parse_args()  # parse the added arguments
        self.replace_string(args)  # pass the parsed arguments into the word replacement method

    # the word replacement method. It one word by another
    def replace_string(self, args):
        if not args.file_name:  # if the file name is not provided, print an error message
            stdout.write("\033[1;31m")
            print("Please provide the target file's name")
        else:  # else continue
            if self.is_binary(args.file_name):  # if the file is a binary file, print an error message
                stdout.write("\033[1;36m")
                print('The target file is a binary file. Please provide text based files')
            else:  # else continue
                try:
                    if not args.old_word:  # if the word to be replaces is not provided, print an error message
                        stdout.write("\033[1;31m")
                        print("Please provide the word you want to replace")
                    elif not args.new_word:  # if the new word is not provided, print an error message
                        stdout.write("\033[1;31m")
                        print("Please provide the new word")
                    else:  # else proceed with the replacement
                        filename = open(args.file_name, 'r+')  # open the file with both read and write permissions
                        file_content = filename.readlines()  # read all the contents form the file
                        for line in file_content:  # loop through the lines in the file
                            self.new_file_content += line  # concatenate the lines' content to the 'new_file_content' variable
                        if args.replacement_count == -1:  # if the replacement count is the default value, replace the word throughout the whole file
                            self.new_file_content = self.new_file_content.replace(args.old_word, args.new_word)
                        elif args.replacement_count < -1:
                            stdout.write("\033[0;31m")
                            print("Please provide a valid word replacement count !")
                        else:  # else if the replacement count is set to another positive value, replace the word up to the number of replacement count
                            self.new_file_content = self.new_file_content.replace(args.old_word, args.new_word, args.replacement_count)
                        filename.seek(0)  # seek the file
                        filename.truncate()  # truncate the file
                        filename.write(self.new_file_content)  # write the new contents to the file
                        stdout.write("\033[0;32m")
                        print("Word Replacement Successful !")  # print a success message to the user
                        filename.close()
                except Exception as e:  # else if there is an error int the whole process, print an error message
                    stdout.write("\033[1;31m")
                    print("Please chech your file name or file path")

    # method to check if a file is a binary file or not
    def is_binary(self, file_name):
        tested_file = open(file_name, 'rb+')  # open file in binary mode
        for line in tested_file:  # loop through the lines of the file
            if b'\0' in line:  # if there is binary data in any of the lines of the file
                self.file_is_binary = True  # set the 'file_is_binary' property of the class to True
                tested_file.close()  # close the file
                return self.file_is_binary  # return the 'file_is_binary' property of the class
        self.file_is_binary = False # set the 'file_is_binary' property of the class to False
        tested_file.close() # close the file
        return self.file_is_binary  # return the 'file_is_binary' property of the class


if __name__ == '__main__':  # if the file is run as a module
    replace_str = ReplaceString()  # create an object of the ReplaceString class
    replace_str.main()  # run the main method
