class Compressor:
    @staticmethod
    def gamma_encode(docIDs):
        encoded_list = []
        prev_docID = 0
        for docID in docIDs:
            gap = docID - prev_docID
            binary_gap = bin(gap)[3:]
            unary_len = "0" * (len(binary_gap) - 1)
            encoded_list.append((unary_len, binary_gap))
            prev_docID = docID
        return encoded_list

    @staticmethod
    def fibonacci_encode(docIDs):
        encoded_list = []
        prev_docID = 0
        for docID in docIDs:
            gap = docID - prev_docID
            fib_seq = Compressor.generate_fibonacci_sequence(gap)
            encoded_str = Compressor.encode_fibonacci_number(fib_seq)
            encoded_list.append(encoded_str)
            prev_docID = docID
        return encoded_list

    @staticmethod
    def generate_fibonacci_sequence(num):
        fib_seq = [1, 2]
        while fib_seq[-1] <= num:
            fib_seq.append(fib_seq[-1] + fib_seq[-2])
        fib_seq.pop()
        return fib_seq

    @staticmethod
    def encode_fibonacci_number(fib_seq):
        encoded_str = ""
        num = fib_seq[-1]
        for fib in reversed(fib_seq[:-1]):
            if num >= fib:
                num -= fib
                encoded_str += "1"
            else:
                encoded_str += "0"
        return "11" + encoded_str + "1"
