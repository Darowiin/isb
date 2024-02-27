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

    def consecutive_bits_test(self) -> float:
        try:
            sum_list = self.sequence.count("1") / self.seq_length
            if abs(sum_list - 0.5) > (2/math.sqrt(self.seq_length)):
                return 0
            
            v_n = 0
            v_n += sum(1 if self.sequence[i] != self.sequence[i+1] else 0 for i in range(self.seq_length-1))
            
            p_value = math.erfc(abs(v_n-2*self.seq_length*sum_list*(1-sum_list))/(2*math.sqrt(2*self.seq_length)*sum_list*(1-sum_list)))
            return p_value
        except ZeroDivisionError as ex:
            logging.error(f"Division by zero: {ex.message}\n{ex.args}\n")