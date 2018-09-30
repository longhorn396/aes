from aes import AESComponent
from common_arrays import isbox, gfp9, gfp11, gfp13, gfp14


class AESDecryptor(AESComponent):

    def aes(self, block, key, nr, verbose):
        """Decrypts a message in 16 byte increments and removes any padding"""
        if verbose:
            self.verbose = True
        output = []
        for i in range(0, len(block), 16):
            output = AESComponent.collapse_matrix(
                self.decipher(block[i:i + 16], key, nr), output)
        output = output[:-1 * output[-1]]
        return output

    def decipher(self, block, key, nr):
        """Decrypts a 4 x 4 array for nr rounds"""
        state = AESComponent.to_col_order_matrix(block)
        self.myprint(state, "init: ")
        state = AESComponent.add_round_key(
            state, AESComponent.to_col_order_matrix(key[-16:]))
        self.myprint(state, "after first round key\n")
        for i in range(nr - 1, 0, -1):
            state = self.shift_rows(state)
            self.myprint(state, str(i) + "\nafter shift rows\n")
            state = self.sub_bytes(state)
            self.myprint(state, "after sub bytes\n")
            state = AESComponent.add_round_key(
                state, AESComponent.to_col_order_matrix(key[16 * i:16 * (i + 1)]))
            self.myprint(state, "after round key\n")
            state = self.mix_columns(state)
            self.myprint(state, "after mix columns\n")
        state = self.shift_rows(state)
        self.myprint(state, "after last shift rows\n")
        state = self.sub_bytes(state)
        self.myprint(state, "after last sub bytes\n")
        state = AESComponent.add_round_key(
            state, AESComponent.to_col_order_matrix(key[:16]))
        self.myprint(state, "final: ")
        return state

    def sub_bytes(self, state):
        return [[isbox[byte] for byte in word] for word in state]

    def shift_rows(self, state):
        return AESComponent.shift_rows(
            state, lambda x, y: (
                x + y) %
            4, lambda x, y: y)

    def mix_columns(self, state):
        return AESComponent.mix_columns(
            state,
            lambda x: gfp14[x],
            lambda x: gfp11[x],
            lambda x: gfp13[x],
            lambda x: gfp9[x])
