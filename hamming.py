class hamming:
    def decode(self, hamming, odd = False):
        w =  self.check(hamming, odd)
        h = list(hamming)
        if w>0 and w<len(hamming):
            print w
            h[w-1] = str(1 - int(h[w-1]))
            correct = "".join(h)
        else:
            correct = hamming
        bits = h[2] + h[4]
        ret = (w==0)
        return (ret, correct, bits)    
        
    
    # check which bit errored        
    def check(self, hamming, odd):
        t1 = self.parity(hamming, [0,2,4], odd) # m1,m3,m5
        t2 = self.parity(hamming, [1,2], odd) # m2,m3
        t4 = self.parity(hamming, [3,4], odd) # m4,m5
        w = int(t4 + t2 + t1, 2)
        return w
    
    # return the hamming code by bits     
    def encode(self, bits, odd):
        """return hamming by bits"""
        e1 = self.parity(bits, [0,1], odd)
        e2 = self.parity(bits, [0], odd)
        e4 = self.parity(bits, [1], odd)
        return e1 + e2 + bits[0] + e4 + bits[1]

    # odd/even check result
    def parity(self, s, indicies, odd):
        """ compute the parity bit """
        sub = ""
        for i in indicies:
            sub += s[i]
        return str((str.count(sub,"1")+odd) % 2)

class hamming2d:
    # encode a 10-bit number 0-1023 , odd parity
    def encode(self,num):
        bits = bin(num)[2:]
        bits = bits.rjust(10,'0')
        # an instance of hamming class
        h1d = hamming()
        h2d = []
        for i in range(0, len(bits), 2):
            b = bits[i:i+2]
            # hamming 1d encode 2 bits to 5 bits, odd parity
            hb = h1d.encode(b,1)
            h2d.append(hb)
        return h2d
        
    # decode a string list h2d, which have 5 * 5 bits   
    def decode(self, h2d):
        total_ret = True
        total_bits = "" 
        for h in h2d:
            # an instance of class hamming
            h1d = hamming()
            # odd parity
            ret, correct, bits = h1d.decode(h,1)
            # and return fag
            total_ret &= ret
            total_bits += bits
        return total_ret, int(total_bits,2)
         
if __name__ == "__main__":
    #test hamming1d
    print "\nhamming 1d\n"
    h = hamming().encode("11",1)
    print h
    ret,correct,bits = hamming().decode("10111",1)
    print ret,correct,bits
    
    #test hamming2d
    print "\nhamming 2d\n"
    h2d = hamming2d().encode(0)
    print h2d
    ret, num =hamming2d().decode(h2d)
    print ret,num
