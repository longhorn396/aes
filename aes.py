#! /usr/local/bin/python3

import sys, getopt
import common_arrays

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
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-k", "--keyfile"):
            key_file = arg
        elif opt in ("-e", "--encrypt") and mode == None:
            mode = 0
        elif opt in ("-d", "--decrypt") and mode == None:
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