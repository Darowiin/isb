import json
import logging
import math


logging.basicConfig(level=logging.INFO)


class NistTest:
    
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence
        self.seq_length = len(sequence)
        
    def bitwise_frequency_test(self) -> float:
        try:
            list = [1 if int(bit) == 1 else -1 for bit in self.sequence]
            sum_list = sum(list)
            
            s_n = math.fabs(sum_list) / math.sqrt(self.seq_length)
            
            p_value = math.erfc(s_n / math.sqrt(2))
            return p_value
        except ZeroDivisionError as ex:
            logging.error(f"Division by zero: {ex.message}\n{ex.args}\n")