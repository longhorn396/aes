clean: 
	@rm cipher
	@rm plaintext

test_128:
	@python aes.py -i test_in -k test_key -o cipher -e
	@python aes.py -i cipher -k test_key -o plaintext -d
	@echo "Encrypted message in cipher file. Decoded message in plaintext file"

test_256:
	@python aes.py -i big_in -k big_key -o cipher -e -s 256
	@python aes.py -i cipher -k big_key -o plaintext -d -s 256
	@echo "Encrypted message in cipher file. Decoded message in plaintext file"
