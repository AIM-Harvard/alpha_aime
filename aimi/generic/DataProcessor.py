from Config import Instance
from modules.convert.DataConverter import DataConverter

class DataProcessor(DataConverter):
    """
    Processor Module.
    Special conversion module that is ment to convert and modify the input data.
    """

    def convert(self, instance: Instance):
        return super().convert(instance)