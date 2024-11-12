import math 

class Posit:
    def __init__(self, nbits, es, value):
        self.nbits = nbits
        self.es = es
        self.value = value
        self.binary = self.encode()

    def encode(self):
        if self.value == 0:
            return '0' * self.nbits

        # sign bit
        sign_bit = '0' if self.value > 0 else '1'
        abs_value = abs(self.value)

        # useed
        useed = 2 ** (2 ** self.es)

        # regime
        k = int(math.log(abs_value, useed))
        regime = '1' * (k + 1) + '0' if k >= 0 else '0' * (-k) + '1'

        # exp
        exponent_bits = ''
        if self.es > 0:
            exponent = int(math.log((abs_value / (useed ** k)),2))
            exponent_bits = f'{exponent:0{self.es}b}'

        # fraction
        fraction = abs_value / (useed ** k)
        if self.es > 0:
            fraction /= (2 ** exponent)
        fraction -= 1 
        fraction_bits = ''
        #print(fraction)
        for _ in range(self.nbits - len(sign_bit) - len(regime) - len(exponent_bits)):
            fraction *= 2
            if fraction >= 1:
                fraction_bits += '1'
                fraction -= 1
            else:
                fraction_bits += '0'

        # combine binary
        posit_bits = sign_bit + regime + exponent_bits + fraction_bits
        return posit_bits[:self.nbits]

    def __lt__(self, other):
        return self.value < other.value
    
    def __repr__(self):
        return f"Posit(nbits={self.nbits}, es={self.es}, value={self.value}, binary={self.binary})"

def float_to_posit(value, nbits=32, es=2):
    return Posit(nbits, es, value)

def float_to_posit_components(value, nbits=32, es=2):
    posit = float_to_posit(value, nbits, es)
    binary = posit.binary

    # get signbit
    sign_bit = binary[0]

    # get regime
    regime_bits = ""
    i = 1
    while i < len(binary) and binary[i] == '1':
        regime_bits += binary[i]
        i += 1
    regime_bits += binary[i] if i < len(binary) else ''

    # get exponent
    exponent_bits = binary[i+1:i+1+es] if i+1+es < len(binary) else binary[i+1:]

    # get fraction
    fraction_bits = binary[i+1+es:] if i+1+es < len(binary) else ''

    return {
        "sign_bit": sign_bit,
        "regime_bits": regime_bits,
        "exponent_bits": exponent_bits,
        "fraction_bits": fraction_bits
    }