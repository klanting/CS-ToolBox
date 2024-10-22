import copy

class AES:
    def __init__(self):
        pass

    def encrypt(self, key: bytes, plaintext: bytes) -> bytes:

        assert len(key) == 16

        AES._key_expansion(key)

        pass

    @staticmethod
    def _key_expansion(key: bytes) -> bytes:
        assert len(key) == 16

        words = [b'' for i in range(4)]
        for i, k in enumerate(key):
            words[i % 4] += k.to_bytes(1, byteorder='big')

        AES._sub_word(words[0])

    @staticmethod
    def _sub_word(word: bytes) -> bytes:
        assert len(word) == 4

        """
        Move first block to the end (1-byte left circular shift)
        """
        to_move = word[0]
        word = word[1:]
        word += to_move.to_bytes(1, byteorder='big')

        AES.calculate_sub_bytes(word[0])

        return word


    @staticmethod
    def calculate_sub_bytes(input_byte: int) -> int:
        """
        Do the calculations of a S-table

        :param input_byte:
        :return:
        """

        """
        take the inverse of the int in finite field 256
        """

        inverse = AES._get_inverse(input_byte, 256)
        print(input_byte, inverse)

    @staticmethod
    def _get_inverse(value: int, field_size: int):
        """
        Determine the inverse in the field using the
        extended algorithm of euclides

        :param value:
        :param field_size:
        :return:
        """

        a = (1, 0, field_size)
        b = (0, 1, value)

        while True:
            b_fits = a[2]//b[2]

            a = tuple([a[i]-b_fits*b[i] for i in range(3)])

            if a[2] == 1:
                return a[1]

            a, b = b, a


if __name__ == "__main__":
    aes_key = b"advancedpassword"

    text = "very highly classified text that only you are allowed to read"

    AES().encrypt(aes_key, text.encode())