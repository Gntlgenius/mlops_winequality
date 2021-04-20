import os
import json



class NotInRange:
    def __init__(self, message = "Values entered are not in range"):
        self.message = message
        super().__init__(self.message)


class NotInColumn:
    def __init__(self, message="Not in column")
    self.message = message
    super().__init__(self.message)