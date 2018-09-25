from aes import AESComponent
from common_arrays import sbox, gfp2, gfp3

def myprint(state, msg):
    out = ""
    for i in range(0, 4):
        for j in range(0, 4):
            out += str(hex(state[j][i])) + " "
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
        myprint(state, "init: ")
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[:16]))
        myprint(state, "after first round key\n")
        for i in range(1, nr):
            print(i)
            state = self.sub_bytes(state)
            myprint(state, "after sub bytes\n")
            state = self.shift_rows(state)
            myprint(state, "after shift rows\n")
            state = self.mix_columns(state)
            myprint(state, "after mix columns\n")
            state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[16*i:16*(i+1)]))
            myprint(state, "after round key\n")
        state = self.sub_bytes(state)
        myprint(state, "after last sub bytes\n")
        state = self.shift_rows(state)
        myprint(state, "after last shift rows\n")
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[-16:]))
        myprint(state, "final: ")
        return state

    def sub_bytes(self, state):
        return [[sbox[byte] for byte in word] for word in state]
    
    def shift_rows(self, state):
        return AESComponent.shift_rows(state, lambda x, y : y, lambda x, y : (x + y) % 4)
    
    def mix_columns(self, state):
        new_state = [word[:] for word in state]
        for i in range(0, 4):
            new_state[0][i] = gfp2[state[0][i]] ^ gfp3[state[1][i]] ^ state[2][i] ^ state[3][i]
            new_state[1][i] = state[0][i] ^ gfp2[state[1][i]] ^ gfp3[state[2][i]] ^ state[3][i]
            new_state[2][i] = state[0][i] ^ state[1][i] ^ gfp2[state[2][i]] ^ gfp3[state[3][i]]
            new_state[3][i] = gfp3[state[0][i]] ^ state[1][i] ^ state[2][i] ^ gfp2[state[3][i]]
        return new_state
