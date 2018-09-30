install:
	pip install -t lib -r requirements.txt

local:
	@python main.py

clean: 
	@rm tests/cipher
	@rm tests/plaintext

test_128:
	@python aes.py -i tests/test_in -k tests/test_key -o tests/cipher -e
	@python aes.py -i tests/cipher -k tests/test_key -o tests/plaintext -d
	@echo "Encrypted message in cipher file. Decoded message in plaintext file"

test_256:
	@python aes.py -i tests/big_in -k tests/big_key -o tests/cipher -e -s 256
	@python aes.py -i tests/cipher -k tests/big_key -o tests/plaintext -d -s 256
	@echo "Encrypted message in cipher file. Decoded message in plaintext file"

test_piazza:
	@./tests/piazza_script.sh