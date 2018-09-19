#! /usr/bin/python3

import sys, getopt, array
import common_arrays, encrypt

class AESComponent:

    @staticmethod
    def to_col_order_matrix(arr):
        matrix = [[0 for _ in range(0, 4)] for _ in range(0, 4)]
        for index, byte, in enumerate(arr):
            matrix[index % 4][index // 4] = byte
        return matrix

    @staticmethod
    def collapse_matrix(matrix, out_array):
        for j in range(0, 4):
            for i in range(0, 4):
                out_array.append(matrix[i][j])
        return out_array
    
    @staticmethod
    def expand_key(key, nk, nr):
        w = [word for word in key]
        for i in range(nk, 4 * (nr + 1)):
            temp = w[4*(i-1):4*i]
            if i % nk == 0:
                temp = [common_arrays.sbox[byte] for byte in temp[1:] + temp[:1]]
                temp[0] = temp[0] ^ common_arrays.Rcon[i // nk]
            elif nk == 8 and i % nk == 4:
                temp = [common_arrays.sbox[byte] for byte in temp]
            for j in range(0, 4):
                w.append(w[4 * (i - nk) + j] ^ temp[j])
        return w
    
    @staticmethod
    def sub_bytes(state, box):
        return [[box[byte] for byte in word] for word in state]
    
    @staticmethod
    def shift_rows(state, l):
        new_state = [word[:] for word in state]
        for i in range(1, len(state)):
            for j in range(0, 4):
                new_state[i][j] = state[i][(l(i, j)) % 4]
        return new_state
    
    @staticmethod
    def add_round_key(state, key):
        for j in range(0, 4):
            for i in range(0, 4):
                state[i][j] ^= key[i][j]
        return state

def print_help(exit_code):
    # TODO: better usage message
    print("usage: aes.py [options]")
    sys.exit(exit_code)

def main(argv):
    input_file = None
    output_file = None
    key_file = None
    mode = None

    try:
      opts, _ = getopt.getopt(argv,"hedi:o:k:",["help","encrypt","decrypt","ifile=","ofile=","kfile="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(0)
        elif opt in ("-i", "--ifile"):
            input_file = open(arg, "rb").read()
        elif opt in ("-o", "--ofile"):
            output_file = open(arg, "wb")
        elif opt in ("-k", "--keyfile"):
            key_file = open(arg, "rb").read()
        elif opt in ("-e", "--encrypt"):
            mode = 0
        elif opt in ("-d", "--decrypt"):
            mode = 1
        
    component = None
    if mode == 0:
        component = encrypt.AESEncryptor()
    if mode == 1:
        import decrypt
        component = decrypt.AESDecryptor()
    
    output = component.aes(input_file, AESComponent.expand_key(key_file, 4, 10), 10)
    output = array.array('B', output)
    output_file.write(output)
    output_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])