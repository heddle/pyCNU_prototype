class Bits:
    @staticmethod
    def check_bit(bits, b):
        return (bits & b) == b

    @staticmethod
    def set_bit(bits, b):
        bits |= b
        return bits

    @staticmethod
    def clear_bit(bits, b):
        bits &= ~b
        return bits

    @staticmethod
    def toggle_bit(bits, b):
        bits ^= b
        return bits

    @staticmethod
    def first_bit(x):
        b = 0
        while x != 0:
            if (x & 1) == 1:
                return b
            x >>= 1
            b += 1
        return -1

    @staticmethod
    def count_bits(x):
        b = 0
        while x != 0:
            if (x & 1) == 1:
                b += 1
            x >>= 1
        return b

    @staticmethod
    def check_bit_long(bits, b):
        return (bits & b) == b

    @staticmethod
    def set_bit_at_location(bits, bit_index):
        bits |= (1 << bit_index)
        return bits

    @staticmethod
    def check_bit_at_location(bits, bit_index):
        bit = (1 << bit_index)
        return Bits.check_bit_long(bits, bit)

    @staticmethod
    def count_bits_long(x):
        b = 0
        while x != 0:
            if (x & 1) == 1:
                b += 1
            x >>= 1
        return b


# Example usage
if __name__ == "__main__":
    print(Bits.check_bit(5, 1))  # Output: True
    print(Bits.set_bit(4, 1))  # Output: 5
    print(Bits.clear_bit(5, 1))  # Output: 4
    print(Bits.toggle_bit(5, 1))  # Output: 4
    print(Bits.first_bit(18))  # Output: 1
    print(Bits.count_bits(15))  # Output: 4
    print(Bits.check_bit_long(5, 1))  # Output: True
    print(Bits.set_bit_at_location(0, 3))  # Output: 8
    print(Bits.check_bit_at_location(8, 3))  # Output: True
    print(Bits.count_bits_long(15))  # Output: 4
