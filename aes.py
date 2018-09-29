#! /usr/bin/python3

import array
import common_arrays
import getopt
import os
import sys


class AESComponent:
    """Class holding common functionality for both encryption and decryption"""

    verbose = False

    def myprint(self, state, msg):
        """If the verbose option is passed at startup, the state will be printed to stdout after every operation"""
        if self.verbose:
            out = ""
            for i in range(0, 4):
                for j in range(0, 4):
                    out += str(hex(state[j][i])) + " "
            print(msg + out)

    @staticmethod
    def to_col_order_matrix(arr):
        """Takes a one-dimensional array of length 16 and turns it into a 4 x 4 array in column first order"""
        matrix = [[0 for _ in range(0, 4)] for _ in range(0, 4)]
        for index, byte, in enumerate(arr):
            matrix[index % 4][index // 4] = byte
        return matrix

    @staticmethod
    def collapse_matrix(matrix, out_array):
        """Takes a 4 x 4 array, flattens it in column first order, and appends it to the out_array"""
        for j in range(0, 4):
            for i in range(0, 4):
                out_array.append(matrix[i][j])
        return out_array

    @staticmethod
    def expand_key(key, nk, nr):
        """Expands the key to a key schedule as described in the ECB standard"""
        w = [word for word in key]
        for i in range(nk, 4 * (nr + 1)):
            temp = w[4*(i-1):4*i]
            if i % nk == 0:
                temp = [common_arrays.sbox[byte]
                        for byte in temp[1:] + temp[:1]]
                temp[0] = temp[0] ^ common_arrays.Rcon[i // nk]
            elif nk == 8 and i % nk == 4:
                temp = [common_arrays.sbox[byte] for byte in temp]
            for j in range(0, 4):
                w.append(w[4 * (i - nk) + j] ^ temp[j])
        return w

    @staticmethod
    def shift_rows(state, f, l):
        """Shifts the order of the elements in the rows of the array
        Parameters f and l are functions that compute the offset to shift the rows by
        """
        new_state = [word[:] for word in state]
        for i in range(1, len(state)):
            for j in range(0, 4):
                new_state[i][f(i, j)] = state[i][(l(i, j))]
        return new_state

    @staticmethod
    def mix_columns(state, f, g, h, l):
        """Mixes the columns by treating them as a four-term polynomial
        Parameters f, g, h, and l are functions that serve as array access or identity depending on encryption or decryption
        """
        new_state = [word[:] for word in state]
        for i in range(0, 4):
            new_state[0][i] = f(state[0][i]) ^ g(
                state[1][i]) ^ h(state[2][i]) ^ l(state[3][i])
            new_state[1][i] = l(state[0][i]) ^ f(
                state[1][i]) ^ g(state[2][i]) ^ h(state[3][i])
            new_state[2][i] = h(state[0][i]) ^ l(
                state[1][i]) ^ f(state[2][i]) ^ g(state[3][i])
            new_state[3][i] = g(state[0][i]) ^ h(
                state[1][i]) ^ l(state[2][i]) ^ f(state[3][i])
        return new_state

    @staticmethod
    def add_round_key(state, key):
        """Adds the current state with the correct portion of the key scedule"""
        for i in range(0, 4):
            for j in range(0, 4):
                state[i][j] ^= key[i][j]
        return state


def print_help(exit_code):
    """Prints the help message and examples of how to run the program"""
    print("usage: aes.py [options]")
    print("\t-h --help\tPrint this message and exit")
    print("\t-v --verbose\tPrint the state after every operation")
    print("\t-i --inputfile\tThe input file (required)")
    print("\t-o --outputfile\tThe output file (required)")
    print("\t-k --keyfile\tThe key file (required)")
    print("\t-m --mode\tEither encrypt or decrypt (required)")
    print("\t-e --encrypt\tAlternate of --mode encrypt")
    print("\t-d --decrypt\tAlternate of --mode decrypt")
    print("\t-s --keysize\tEither 128 (default) or 256")
    print("Examples:")
    print("python aes.py -i test_in -k test_key -o cipher -e --verbose")
    print("python aes.py -i cipher -k big_key -o plaintext -d -s 256")
    sys.exit(exit_code)


def open_and_read(fName):
    """Helper method to open and read files"""
    if os.path.exists(fName):
        with open(fName, "rb") as f:
            try:
                bytes = f.read()
                f.close()
                return bytes
            except Exception:
                sys.stderr.write(
                    "Error reading files. Please make sure they exist and are readable\n")
                print_help(-1)
    sys.stderr.write("Error reading files. Please make sure they exist\n")
    print_help(-1)


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
        opts, _ = getopt.getopt(argv, "hvedi:o:k:s:m:", [
                                "help", "verbose", "encrypt", "decrypt", "inputfile=", "outputfile=", "keyfile=", "keysize=", "mode="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(0)
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-i", "--inputfile"):
            input_file = open_and_read(arg)
        elif opt in ("-o", "--outputfile"):
            output_file = open(arg, "wb")
        elif opt in ("-k", "--keyfile"):
            key_file = open_and_read(arg)
        elif opt in ("-s", "--keysize"):
            key_size = int(arg)
            if key_size != 256 and key_size != 128:
                print_help(-1)
        elif opt in ("-e", "--encrypt") or (opt in ("-m", "--mode") and arg == "encrypt"):
            mode = 0
        elif opt in ("-d", "--decrypt") or (opt in ("-m", "--mode") and arg == "decrypt"):
            mode = 1

    if input_file == None or key_file == None or output_file == None or mode == None:
        print_help(-1)
    elif key_size != 8 * len(key_file):
        sys.stderr.write("Mismatching key sizes\n")
        print_help(-1)

    component = None
    if mode == 0:
        import encrypt
        component = encrypt.AESEncryptor()
    if mode == 1:
        import decrypt
        component = decrypt.AESDecryptor()

    output = component.aes(bytearray(input_file), AESComponent.expand_key(
        key_file, nk[key_size], nr[key_size]), nr[key_size], verbose)
    output = array.array('B', output)
    output_file.write(output)
    output_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
