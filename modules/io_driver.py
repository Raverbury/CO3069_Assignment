class IODriver:
    def write_to(data):
        pass

    def read_from():
        pass

class FileDriver(IODriver):
    def __init__(self, file_name):
        self.file_name = file_name

    def read_from(self, ):
        with open(self.file_name, "r") as f:
            data = f.read()
            f.close()
        return data

    def write_to(self, data):
        with open(self.file_name, "w") as f:
            f.write(data)
            f.close()

