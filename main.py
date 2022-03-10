import string
import csv
from queue import Queue
from threading import Thread, Lock
import time
import os


class MirrorEncryption:
    def __init__(self, data_source="input2.csv", output_file_name="output.csv", thread_count=10):
        self.read_file = data_source
        self.q = Queue()
        self.thread_count = thread_count
        self.output = tuple()
        self.output_file_name = output_file_name
        self.start_time = ""
        self.file_size = os.path.getsize(data_source)

    def read_as_csv(self):
        print("=======================================")
        print(f"Reading {self.read_file}.......")
        print("File Size is :", self.file_size, "bytes")
        self.start_time = time.process_time()
        with open(self.read_file, "r", newline='') as my_input_file:
            content = csv.reader(my_input_file)
            for line in content:
                yield line

    def read_as_text(self):
        print("================================================")

        print(f"Reading {self.read_file}.......")
        print("File Size is :", self.file_size, "bytes")
        self.start_time = time.process_time()
        my_input_file = open(self.read_file, "r")
        content = my_input_file.read()
        content_list = content.splitlines()
        my_input_file.close()
        yield content_list

    def get_mirror(self, seq):
        string_list = list(string.ascii_lowercase)

        def func(char):
            lower_char = char.lower()
            if lower_char in string_list:
                if char.isupper():
                    char = string_list[-1 - (string_list.index(lower_char))].upper()
                else:
                    char = string_list[-1 - (string_list.index(lower_char))]
            return char

        result = list(map(func, seq))
        n = ''.join([str(elem) for elem in list(result)])
        return n

    def encrypt(self, input):

        def local_worker(q, lock):
            while True:
                value = q.get()
                with lock:
                    self.output = self.output + ((self.get_mirror(value),),)
                q.task_done()

        if input == 1:
            for x in self.read_as_csv():
                if x:
                    self.q.put(x[0])
        elif input == 2:
            for x in list(self.read_as_text())[0]:
                if x != "":
                    self.q.put(x)
        lock = Lock()
        for i in range(self.thread_count):
            t = Thread(name=f"Thread{i + 1}", target=local_worker, args=(self.q, lock))
            t.daemon = True  # dies when the main thread dies
            t.start()
        self.q.join()
        csvfile = open(self.output_file_name, 'w', newline='')
        obj = csv.writer(csvfile)
        obj.writerows(((self.output)))
        print(f"Total time : {time.process_time() - self.start_time}")
        print("================================================")

    @staticmethod
    def custom_def():
        str = """
        ========================================================
        MirrorEncryption class includes two different approaches 
                1.	Reading CSV as CSV file 
                2.	Reading CSV as text file.
            Reading CSV as text file is much efficient then reading as CSV file.
            Apart from these two there we can also using third party library like Dask , for this application I have not used any third party package.
            This also includes test case 
                
            Dependencies
                Python 3.8.0
                pytest-7.0.1
                
            Key features:
                . Class base approach
                . Used multithreading queue
                . Tried to maintain the order by using tuple
                . Displaying the execution time to evaluate the performance
                . The setup includes a test csv file of 247 mb input.csv
                
            ================================================================
            """
        print(str)


if __name__ == "__main__":

    obj = MirrorEncryption("data.csv", "output.csv")
    while True:
        print("There are two different approach used")
        print("To read as csv press 1 :")
        print("To read as text press 2 :")
        print("For overview press 3 :")
        i = input("Please select ")

        if i == "1":
            obj.encrypt(1)
        elif i == "2":
            obj.encrypt(2)
        elif i == "3":
            obj.custom_def()
        else:
            exit()
