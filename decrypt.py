from aes import AESComponent
from common_arrays import isbox, gfp9, gfp11, gfp13, gfp14

def myprint(state, msg):
    out = []
    for i in range(0, 4):
        for j in range(0, 4):
            print(str(i) + ' ' + str(j))
            out += state[i][j]
    print(msg + out)

class AESDecryptor(AESComponent):

    def aes(self, block, key, nr):
        output = []
        for i in range(0, len(block), 16):
            output = AESComponent.collapse_matrix(self.decipher(block[i:i+16], key, nr), output)
        # Remove padding
        # output = output[:-1 * output[-1]]
        return output
    
    def decipher(self, block, key, nr):
        print(block)
        state = AESComponent.to_col_order_matrix(block)
        print(state)
        state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[-16:]))
        # print(state)
        # myprint("after first round", state)
        for i in range(nr - 1, 0, -1):
            # print(i)
            state = self.shift_rows(state)
            myprint("after shift", state)
            state = self.sub_bytes(state)
            state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[16*i:16*(i+1)]))
            state = self.mix_columns(state)
        state = self.shift_rows(state)
        state = self.sub_bytes(state)
        state = state = AESComponent.add_round_key(state, AESComponent.to_col_order_matrix(key[:16]))
        return state

    def sub_bytes(self, state):
        return AESComponent.sub_bytes(state, isbox)
    
    def shift_rows(self, state):
        return AESComponent.shift_rows(state, lambda x, y: x - y)
    
    def mix_columns(self, state):
        temp = [0 for _ in range(0, 4)]
        for i in range(0, 4):
            temp[0] = (gfp14[state[0][i]] ^ gfp11[state[1][i]]) ^ (gfp13[state[2][i]] ^ gfp9[state[3][i]])
            temp[1] = (gfp9[state[0][i]] ^ gfp14[state[1][i]]) ^ (gfp11[state[2][i]] ^ gfp13[state[3][i]])
            temp[2] = (gfp13[state[0][i]] ^ gfp9[state[1][i]]) ^ (gfp14[state[2][i]] ^ gfp11[state[3][i]])
            temp[3] = (gfp11[state[0][i]] ^ gfp13[state[1][i]]) ^ (gfp9[state[2][i]] ^ gfp14[state[3][i]])
            for j in range(0, 4):
                state[j][i] = temp[j]
        return state
