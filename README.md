# CS 361 AES Assignment

## Explanation

My two test cases were taken from [this example](https://kavaliro.com/wp-content/uploads/2014/03/AES.pdf) as I preferred it to the walkthroughs in the NIST document for debugging.

I also made a web UI for this project. For more information on that, see [here](README.md#web).

### AESComponent

#### myprint

Prints the round number, latest operation performed, and the current (flattened) state in column major order if the program is run with the `--verbose` option.

#### to_col_order_matrix

Since AES was originally standardized with column-major arrays, I chose to do the same. This is a helper method that transforms a block of the cipher or plaintext into a 4 x 4 column-major order array.

#### collapse_matrix

Takes in a 4 x 4 column-major array and a flat array, appends the flattened first array to the second and returns the result.

#### expand_key

Takes either a 128 or 256 bit key and expands it to a key schedule as described in the NIST paper. The schedule contains the original key as the first words. Every following word is the result of an XOR operation on the immediately previous word and the word nk positions earlier. If the position is a multiple of nk, the bytes in the word are shifted left by one position, substituted by the bytes in the sbox array, and the new first byte is XOR'd with a round constant. If the original key is 256 bits and the position is a muliple of 4, the same transformation will be applied without the shift and round constant. In both cases, the first XOR described still takes place.

#### shift_rows (common)

Takes in a state and two functions, one of which is the identity. It creates a copy of the state before shifting the bytes in the four rows of the new state by 0, 1, 2, and 3 respectively and returns. The direction of the shift is determined by which function returns the raw column number as opposed to the computed index.

#### mix_columns (common)

Takes in a state and four functions either acting as array accesses or identities. It creates a copy of the state and essentially turns that copy into the result of a matrix by matrix multiplication of the original state and a fixed matrix, where multiplicaiton of bytes means a table lookup and addition means XOR. It returns the result of this multiplication.

#### add_round_key

Takes in a state and part of the key schedule. It returns the state after each byte has been XOR'd with the corresponding byte in the schedule subset. The same code is used in both encryption and decryption.

### AESEncryptor

#### aes (encryption)

Takes in an array of bytes from the raw message, the key schedule, the number of rounds, and the verbose boolean. If verbose is set to true, then the object will save that value for later in the cipher function. It pads the raw message to a muliple of 16 using zeros with the last byte saying how many bytes were padded to the message. The function then calls the cipher function on each 16 byte part of the message and returns the encrypted message.

#### cipher

Takes a part of the raw message, the key schedule, and the number of rounds. It transforms the message part to a two dimensional array. If the verbose option was passed at startup, the state will be printed. To save time, this is the only verbose message that will be mentioned here. Then it adds the round 0 key to the state. For each round from 1 to nr - 1 (inclusive), it calls sub_bytes, shift_rows, mix_columns, and add_round_key on the state, with the appropriate part of the key schedule being added to the state in add_round_key. For the last round, it will call sub_bytes, shift rows, and add_round_key (no mix_columns) and return the result.

#### sub_bytes (encryption)

Takes in the state. It looks up each byte in each word in the state and substitutes them by using the value as an index for sbox. It returns the state with all bytes substituted.

#### shift_rows (encryption)

Take in the state. Passes the state, an identity function, and the function that determines how much to shift the rows by to AESComponent.shift_rows. Passing the functions in this way shifts the bytes in the rows to the left by the desired ammounts.

#### mix_columns (encryption)

Takes in the state. Passes the state, two array access functions and two identity funcitons to AESComponent.mix_columns. The combination of these two functions acheives the same result as the multiplication of the static matrix and the state described in the NIST document.

### AESDecryptor

#### aes (decryption)

Takes in an array of bytes from the cipher, the key schedule, the number of rounds, and the verbose boolean. If verbose is set to true, then the object will save that value for later in the decipher function. The function then calls the cipher function on each 16 byte part of the cipher, removes the zero length padding, and returns the decrypted message.

#### decipher

Takes a part of the cipher, the key schedule, and the number of rounds. It transforms the cipher part to a two dimensional array. If the verbose option was passed at startup, the state will be printed. To save time, this is the only verbose message that will be mentioned here. Then it adds the final round key to the state. For each round from nr - 1 to 1 (inclusive), it calls shift_rows, sub_bytes, add_round_key, and mix columns on the state, with the appropriate part of the key schedule being added to the state in add_round_key. For the last round, it will call shift rows ,sub_bytes, and add_round_key (no mix_columns) and return the result.

#### sub_bytes (decryption)

Takes in the state. It looks up each byte in each word in the state and substitutes them by using the value as an index for isbox. It returns the state with all bytes substituted.

#### shift_rows (decryption)

Take in the state. Passes the state, the function that determines how much to shift the rows by, and an identity function to AESComponent.shift_rows. Passing the functions in this way shifts the bytes in the rows to the right by the desired ammounts.

#### mix_columns (decryption)

Takes in the state. Passes the state and four array access functions to AESComponent.mix_columns. The combination of these two functions acheives the same result as the multiplication of the static matrix and the state described in the NIST document.

### Common Arrays

The contents of common_arrays.py were taken from [this GitHub repo](https://github.com/pcaro90/Python-AES/blob/master/AES_base.py).

### Other

#### print_help

Prints the possible arguments to the program and some examples before exiting.

#### open_and_read

A helper method to safely open files. Takes in a file name, checks to see if it exists, trys to open it, read from it, and close it. If it can, the read bytes will be returned.

#### main

The runner method. Parses arguments, checks for missing requirements, and calls the aes method on the appropriate component before taking the cipher or plaintext, writes them to the appropriate file and closing it.

### <a name="web"></a>Web UI

The UI is a simple Flask application that runs locally at `127.0.0.1:80`. All the logic can be found in main.py and is very similar to the main function in aes.py, but without some of the argument checking and validatoin as I leave some of that to the HTML form. I also allow the user to specify thier own filename and extension to make opening downloaded files from the browser easier.

## How to Run

### Make rules

* install     - installs dependencies for web UI in lib directory
* local       - starts local web server and prints IP address
* clean       - removes files generated by tests below
* test_128    - encodes and decodes the message in test_in
* test_256    - encodes and decodes the message in big_in
* test_piazza - runs the script that was posted by a classmate on Piazza

### Manually

Run `python aes.py --help` for complete list of options and examples

```bash
usage: aes.py [options]
        -h --help       Print this message and exit
        -v --verbose    Print the state after every operation
        -i --inputfile  The input file (required)
        -o --outputfile The output file (required)
        -k --kfile      The key file (required)
        -m --mode       Either encrypt or decrypt (required)
        -e --encrypt    Alternate of --mode encrypt
        -d --decrypt    Alternate of --mode decrypt
        -s --keysize    Either 128 (default) or 256
```

## Contact

If for whatever reason something comes up you can email me at devin@drawhorn.com
