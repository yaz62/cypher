from utils import ALPHABET

def get_inv_map(map_dict):
    inv_map = {v: k for k, v in map_dict.items()}
    return inv_map


def rotate_dict(map_dict, n):
    '''
        rotates the dictionary such that k_(i+1): v_i
    '''
    keys = list(map_dict.keys())
    values = list(map_dict.values())
    length = len(values)

    if length == 0:
        return {}

    n = n % length

    rotated_values = values[-n:] + values[:-n]

    return dict(zip(keys, rotated_values))


def rotate_string(s, n):
    """
        rotates a string by `n` positions.
    """
    n = n % len(s)
    return s[-n:] + s[:-n]


class Scrambler:
    def __init__(self, input: str, output: str):
        if len(input) != len(output):
            raise Exception("Input and output lengths do not match.")
        self.input = input
        self.output = output

    def rotate(self, n: int, in_place=False):
        input, output = rotate_string(self.input, n), rotate_string(self.output, n)

        if in_place:
            self.input, self.output = input, output
        else:
            return input, output
        
    def print(self, n: int=0):
        input, output = self.rotate(n)
        print(f"{input}\n{output}")


class Scramblers:
    def __init__(self, *scramblers: Scrambler, init_key: str=None, input: str=ALPHABET, output: str=ALPHABET):
        self.input, self.output = input, output
        self.scramblers = scramblers

        if init_key is not None:
            if len(init_key) != len(scramblers):
                raise Exception("Key length should match number of scramblers!")
            
            for i, k in enumerate(init_key):
                r = scramblers[i].input.index(k)
                scramblers[i].rotate(-r, in_place=True)

    def get_mappings(self, rot_nums):
        # get rotated inputs and outputs
        inputs, outputs = [], []
        for i, s in enumerate(self.scramblers):
            inp, out = s.rotate(rot_nums[i])
            inputs.append(inp)
            outputs.append(out)

        S = []
        S.append({k: v for k, v in zip(self.input, inputs[0])})

        for i in range(1, len(inputs)):
            S.append({k: v for k, v in zip(outputs[i-1], inputs[i])})

        S.append({k: v for k, v in zip(outputs[-1], self.output)})

        return S, [get_inv_map(s) for s in S]
    
    def forward(self, c: str, rot_num: int):
        '''
            runs scramblers forward. 
        '''
        Ss, _ = self.get_mappings(rot_num)

        x = c
        for S in Ss:
            x = S[x]

        return x
    
    def backward(self, c: str, rot_num: int):
        '''
            runs scramblers backward. 
        '''
        _, Ss = self.get_mappings(rot_num)

        x = c
        for S in Ss[::-1]:
            x = S[x]

        return x
    
    def print(self, rot_num: int=0):
        print_str = self.input + "\n\n"

        for s in self.scramblers:
            input, output = s.rotate(rot_num)
            print_str += input + '\n' + output + '\n\n'
        
        print_str += self.output

        print(print_str)