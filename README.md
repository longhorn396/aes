# CS 361 AES Assignment

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
