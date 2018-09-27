# CS 361 AES Assignment

## Explanation

### AESComponent

#### myprint

Prints the round number, latest operation performed, and the current (flattened) state in column major order if the program is run with the `--verbose` option.

#### to_col_order_matrix

Since AES was originally standardized with column-major arrays, I chose to do the same. This is a helper method that transforms a block of the cipher or plaintext into a 4 x 4 column-major order array.

#### collapse_matrix

Takes in a 4 x 4 column-major array and a flat array, appends the flattened first array to the second and returns the result.

#### expand_key

Takes either a 128 or 256 bit key and expands it to a key schedule as described in the NIST paper. The schedule contains the original key as the first words. Every following word is the result of an XOR operation on the immediately previous word and the word nk positions earlier. If the position is a multiple of nk, the bytes in the word are shifted left by one position, substituted by the bytes in the sbox array, and the new first byte is XOR'd with a round constant. If the original key is 256 bits and the position is a muliple of 4, the same transformation will be applied without the shift and round constant. In both cases, the first XOR described still takes place.

#### shift_rows

Takes in a state and two functions, one of which is the identity. It creates a copy of the state before shifting the bytes in the four rows of the new state by 0, 1, 2, and 3 respectively and returns. The direction of the shift is determined by which function is the identity.

#### mix_columns

Takes in a state and four functions either acting as array accesses or identities. It creates a copy of the state and essentially turns that copy into the result of a matrix by matrix multiplication of the original state and a fixed matrix, where multiplicaiton of bytes means a table lookup and addition means XOR. It returns the result of this multiplication.

#### add_round_key

Takes in a state and part of the key schedule. It returns the state after each byte has been XOR'd with the corresponding byte in the schedule subset.

### AESEncryptor

### AESDecryptor

### Common Arrays

### Other

#### print_help

Prints the possible arguments to the program and some examples before exiting.

#### open_and_read

A helper method to safely open files. Takes in a file name, checks to see if it exists, trys to open it, read from it, and close it. If it can, the read bytes will be returned.

#### main

The runner method. Parses arguments, checks for missing requirements, and calls the aes method on the appropriate component before taking the cipher or plaintext, writes them to the appropriate file and closing it.

## How to Run

### Requirements

* Python 3 (in PATH as python)
* make

### Make rules

* test_128 - encodes and decodes the message in test_in
* test_256 - encodes and decodes the message in big_in

### Manually

Run `python aes.py --help` for complete list of options and examples

```bash
usage: aes.py [options]
        -h --help       Print this message
        -v --verbose    Print the state after every operation
        -e --encrypt    Encrypt the message
        -d --decrypt    Decrypt the message
        -i --ifile      The input file (required)
        -o --ofile      The output file (required)
        -k --kfile      The key file (required)
        -s --keysize    Either 128 (default) or 256
```

## Contact

If for whatever reason something comes up you can email me at devin@drawhorn.com
