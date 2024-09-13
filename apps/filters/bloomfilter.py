import math
import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, items_count: int, fp_prob: float) -> None:
        """
        items_count : int
            Number of items expected to be stored in bloom filter
        fp_prob : float
            False Positive probability in decimal
        """
        # False possible probability in decimal
        self.fp_prob = fp_prob

        # Size of bit array to use
        self.size = self.get_size(items_count, fp_prob)
        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items_count)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)


    def add(self, item) -> bool:
        digests = []
        for i in range(self.hash_count):
            # create digest for given item.
            # i work as seed to mmh3.hash() function
            # With different seed, digest created is different
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)

            # set the bit True in bit_array
            self.bit_array[digest] = True
        return True


    def check(self, item) -> bool:
        """
        Check for existence of an item in filter
        """
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:

                # if any of bit is False then,its not present
                # in filter
                # else there is probability that it exist
                return False
        return True


    @classmethod
    def get_size(cls, items_count: int, fp_prob: float) -> int:
        """
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        items_count : int
            number of items expected to be stored in filter
        fp_prob : float
            False Positive probability in decimal
        """
        m = -(items_count * math.log(fp_prob))/(math.log(2)**2)
        return int(m)


    @classmethod
    def get_hash_count(cls, bit_array_size: int, items_count: int) -> int:
        '''
        Return the hash function(k) to be used using
        following formula
        k = (m/n) * lg(2)

        bit_array_size : int
            size of bit array
        items_count : int
            number of items expected to be stored in filter
        '''
        k = (bit_array_size/items_count) * math.log(2)
        return int(k)
