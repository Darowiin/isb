import json
import logging
import math

import mpmath

logging.basicConfig(level=logging.INFO)

pi = {0: 0.2148, 1: 0.3672, 2: 0.2305, 3: 0.1875}

class NistTest:
    
    def __init__(self, sequence: str) -> None:
        self.sequence = sequence
        self.seq_length = len(sequence)
        self.MAX_LENGTH_BLOCK = 8
        
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
            
    def longest_sequence_units_test(self) -> float:
        try:
            block_max_len = {}
            for step in range(0, self.seq_length, self.MAX_LENGTH_BLOCK):
                block = self.sequence[step:step + self.MAX_LENGTH_BLOCK]
                max_length = length = 0
                for bit in block:
                    length = length + 1 if bit == "1" else 0
                    max_length = max(max_length, length)
                block_max_len[max_length] = block_max_len.get(max_length, 0) + 1

            v_n = {1: 0, 2: 0, 3: 0, 4: 0}
            for i in block_max_len:
                key = min(i, 4)
                v_n[key] += block_max_len[i]

            xi_square = 0
            for i in range(4):
                xi_square += math.pow(v_n[i + 1] - 16 * pi[i], 2) / (16 * pi[i])
                
            return mpmath.gammainc(3 / 2,  xi_square / 2)
        except Exception as ex:
            logging.error(f"Error occurred during the test execution: {ex.message}\n{ex.args}\n")