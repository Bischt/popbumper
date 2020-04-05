from tabulate import tabulate


class Table:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

    def display(self, fmt=None):
        """
        Display data in tabular format with headers using tabulate
        :param fmt:
        :return: 
        """
        print(tabulate(self.data, headers=self.headers, tablefmt="plain"))
