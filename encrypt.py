from aes import AESComponent
from common_arrays import sbox, gfp2, gfp3

class AESEncryptor(AESComponent):

    def aes(self, block, key, nr):
        # pad = 16 - (len(block) % 16)
        # block.extend([0] * pad)
        # block[-1] = pad
        output = []
        for i in range(0, len(block), 16):
            output = AESComponent.collapse_matrix(self.cipher(block[i:i+16], key, nr), output)
        return output
    
    def cipher(self, block, key, nr):
        state = AESComponent.to_col_order_matrix(block)
        self.myprint(state, "init: ")
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[:16]))
        self.myprint(state, "after first round key\n")
        for i in range(1, nr):
            print(i)
            state = self.sub_bytes(state)
            self.myprint(state, "after sub bytes\n")
            state = self.shift_rows(state)
            self.myprint(state, "after shift rows\n")
            state = self.mix_columns(state)
            self.myprint(state, "after mix columns\n")
            state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[16*i:16*(i+1)]))
            self.myprint(state, "after round key\n")
        state = self.sub_bytes(state)
        self.myprint(state, "after last sub bytes\n")
        state = self.shift_rows(state)
        self.myprint(state, "after last shift rows\n")
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[-16:]))
        self.myprint(state, "final: ")
        return state

    def sub_bytes(self, state):
        return [[sbox[byte] for byte in word] for word in state]
    
    def shift_rows(self, state):
        return AESComponent.shift_rows(state, lambda x, y : y, lambda x, y : (x + y) % 4)
    
    def mix_columns(self, state):
        return AESComponent.mix_columns(state, lambda x: gfp2[x], lambda x: gfp3[x], lambda x: x, lambda x: x)
