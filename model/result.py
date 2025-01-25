import pandas as pd


class Result:
    MESSAGE = 'Message'
    RESPONSE = 'Response'
    COLUMNS = [MESSAGE, RESPONSE]

    def __init__(self, data, columns):
        if data[0][1] != 0:
            self.table = pd.DataFrame(data=data, columns=self.COLUMNS)
            self.msg = self.table.iat[0, 0]
            self.status_code = int(self.table.iat[0, 1])
            self.success = False

        else:
            self.table = pd.DataFrame(data=data, columns=columns)
            self.msg = self.table.iat[0, 0]
            self.status_code = int(self.table.iat[0, 1])
            self.success = True

    def is_success(self) -> bool:
        return self.success

    @staticmethod
    def exception_result(ex: Exception):
        data = [[str(ex), -1]]
        return Result(data, Result.COLUMNS)
