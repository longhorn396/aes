from aes import AESComponent
from common_arrays import sbox, gfp2, gfp3

def myprint(state, msg):
    out = ""
    for i in range(0, 4):
        for j in range(0, 4):
            out += str(hex(state[i][j])) + " "
    print(msg + out)

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
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[:16]))
        for i in range(1, nr):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[16*i:16*(i+1)]))
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[-16:]))
        return state

    def sub_bytes(self, state):
        return AESComponent.sub_bytes(state, sbox)
    
    def shift_rows(self, state):
        return AESComponent.shift_rows(state, lambda x, y : x + y)
    
    def mix_columns(self, state):
        temp = [0 for _ in range(0, 4)]
        for i in range(0, 4):
            temp[0] = gfp2[state[0][i]] ^ gfp3[state[1][i]] ^ state[2][i] ^ state[3][i]
            temp[1] = state[0][i] ^ gfp2[state[1][i]] ^ gfp3[state[2][i]] ^ state[3][i]
            temp[2] = state[0][i] ^ state[1][i] ^ gfp2[state[2][i]] ^ gfp3[state[3][i]]
            temp[3] = gfp3[state[0][i]] ^ state[1][i] ^ state[2][i] ^ gfp2[state[3][i]]
            for j in range(0, 4):
                state[j][i] = temp[j]
        return state