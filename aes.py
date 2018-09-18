#! /usr/local/bin/python3

import sys, getopt
import common_arrays
import encrypt

class AESComponent:

    def to_col_order_matrix(arr):
        matrix = [[0 for _ in range(0, 4)] for _ in range(0, 4)]
        index = 0
        for byte in arr:
            matrix[index % 4][index // 4] = byte
            index += 1
        return matrix

    def collapse_matrix(matrix, out_array):
        for j in range(0, 4):
            for i in range(0, 4):
                out_array.append(matrix[i][j])

    def add_round_key(matrix, key, index):
        for j in range(0, 4):
            for i in range(0, 4):
                matrix[i][j] ^= key[index]
                index += 1
        return matrix

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
      opts, args = getopt.getopt(argv,"hedi:o:k:",["help","encrypt","decrypt","ifile=","ofile=","kfile="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help(0)
        elif opt in ("-i", "--ifile"):
            input_file = bytearray(open(arg, "rb").read())
        elif opt in ("-o", "--ofile"):
            output_file = open(arg, "wb")
        elif opt in ("-k", "--keyfile"):
            key_file = bytearray(open(arg, "rb").read())
        elif opt in ("-e", "--encrypt"):
            mode = 0
        elif opt in ("-d", "--decrypt"):
            mode = 1
    
    i = bytearray(open(input_file, "rb").read())
    k = bytearray(open(input_file, "rb").read())
    o = open(output_file, "wb")

    print("Read files, input is {0} in length, key is {1} in length".format(len(i), len(k)))
    print("input:")
    print(i)
    print("key")
    print(k)

if __name__ == "__main__":
    main(sys.argv[1:])