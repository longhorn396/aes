#! /usr/bin/python3

import sys, getopt, array
import common_arrays

class AESComponent:

    verbose = False

    def myprint(self, state, msg):
        if self.verbose:
            out = ""
            for i in range(0, 4):
                for j in range(0, 4):
                    out += str(hex(state[j][i])) + " "
            print(msg + out)

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
    def shift_rows(state, f, l):
        new_state = [word[:] for word in state]
        for i in range(1, len(state)):
            for j in range(0, 4):
                new_state[i][f(i, j)] = state[i][(l(i, j))]
        return new_state
    
    @staticmethod
    def mix_columns(state, f, g, h, l):
        new_state = [word[:] for word in state]
        for i in range(0, 4):
            new_state[0][i] = f(state[0][i]) ^ g(state[1][i]) ^ h(state[2][i]) ^ l(state[3][i])
            new_state[1][i] = l(state[0][i]) ^ f(state[1][i]) ^ g(state[2][i]) ^ h(state[3][i])
            new_state[2][i] = h(state[0][i]) ^ l(state[1][i]) ^ f(state[2][i]) ^ g(state[3][i])
            new_state[3][i] = g(state[0][i]) ^ h(state[1][i]) ^ l(state[2][i]) ^ f(state[3][i])
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
    verbose = False
    input_file = None
    output_file = None
    key_file = None
    key_size = 128
    mode = None
    nk = {128:  4, 256:  8}
    nr = {128: 10, 256: 14}

    try:
      opts, _ = getopt.getopt(argv,"hvedi:o:k:s:",["help","verbose","encrypt","decrypt","ifile=","ofile=","kfile=","keysize="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(0)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-i", "--ifile"):
            input_file = open(arg, "rb").read()
        elif opt in ("-o", "--ofile"):
            output_file = open(arg, "wb")
        elif opt in ("-k", "--keyfile"):
            key_file = open(arg, "rb").read()
        elif opt in ("-s", "--keysize"):
            key_size = int(arg)
            if key_size != 256 and key_size != 128: print_help(-1)
        elif opt in ("-e", "--encrypt"):
            mode = 0
        elif opt in ("-d", "--decrypt"):
            mode = 1
        
    component = None
    if mode == 0:
        import encrypt
        component = encrypt.AESEncryptor()
    if mode == 1:
        import decrypt
        component = decrypt.AESDecryptor()
    
    output = component.aes(input_file, AESComponent.expand_key(key_file, nk[key_size], nr[key_size]), nr[key_size], verbose)
    output = array.array('B', output)
    output_file.write(output)
    output_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])