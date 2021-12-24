from heapq import heapify, heappop, heappush
import pickle


class HeapNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, node):
        return self.freq < node.freq

    def __eq__(self, node):
        if not node or not isinstance(node, HeapNode):
            return False
        return self.freq == node.freq

    def __str__(self):
        s = f'{self.char if self.char else ""}'
        if self.left or self.right:
            s += f'[{self.left},{self.right}]'
        return s


class HuffmanCoding:
    @staticmethod
    def make_freq_dict(text):
        frequency = {}
        for c in text:
            if c not in frequency:
                frequency[c] = 0
            frequency[c] += 1
        return frequency

    @staticmethod
    def make_heap(frequency):
        heap = [HeapNode(k, v) for k, v in frequency.items()]
        heapify(heap)
        return heap

    @staticmethod
    def merge_nodes(heap):
        while len(heap) > 1:
            left, right = heappop(heap), heappop(heap)
            new_freq = left.freq + right.freq
            heappush(heap, HeapNode(None, new_freq, left, right))
        return heap

    @staticmethod
    def make_codes_helper(codes, root, cur_code):
        if not root:
            return
        if root.char:
            codes[root.char] = cur_code
            return

        HuffmanCoding.make_codes_helper(codes, root.left, cur_code+'0')
        HuffmanCoding.make_codes_helper(codes, root.right, cur_code+'1')

    @staticmethod
    def make_codes(heap):
        root = heappop(heap)
        codes = {}
        HuffmanCoding.make_codes_helper(codes, root, '')
        return codes

    @staticmethod
    def encode_text(codes, text):
        encoded_text = ''.join([codes[c] for c in text])
        return encoded_text

    @staticmethod
    def decode_text(reverse, encoded_text):
        cur_code = ''
        decoded_text = ''

        for bit in encoded_text:
            cur_code += bit
            if cur_code in reverse:
                character = reverse[cur_code]
                decoded_text += character
                cur_code = ''

        return decoded_text

    @staticmethod
    def pad_text(text):
        extra_padding = 8 - len(text) % 8
        text += '0' * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        text = padded_info + text
        return text

    @staticmethod
    def unpad_text(padded_text):
        padded_info = padded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_text = padded_text[8:]
        text = padded_text[:-1 * extra_padding]
        return text

    @staticmethod
    def get_byte_array(padded_text):
        if len(padded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_text), 8):
            byte = padded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, in_path, out_path, out_pickle):
        with open(in_path, 'r') as in_file, open(out_path, 'wb') as out_file:
            text = in_file.read().rstrip()

            frequency = self.make_freq_dict(text)
            print(frequency)
            heap = self.make_heap(frequency)
            heap = self.merge_nodes(heap)
            print(heap[0])
            codes = self.make_codes(heap)
            print(codes)

            with open(out_pickle, 'wb') as f:
                # pickle.dump(codes, f, pickle.HIGHEST_PROTOCOL)
                pickle.dump(frequency, f, pickle.HIGHEST_PROTOCOL)

            encoded_text = self.encode_text(codes, text)
            padded_text = self.pad_text(encoded_text)

            b = self.get_byte_array(padded_text)
            out_file.write(bytes(b))

    def decompress(self, in_path, out_path, in_pickle):
        with open(in_path, 'rb') as file, open(out_path, 'w') as output:
            bit_string = ''

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.unpad_text(bit_string)

            with open(in_pickle, 'rb') as f:
                frequency = pickle.load(f)
                heap = self.make_heap(frequency)
                heap = self.merge_nodes(heap)
                codes = self.make_codes(heap)
                # codes = pickle.load(f)
                reverse = {value: key for (key, value) in codes.items()}

            decompressed_text = self.decode_text(reverse, encoded_text)

            output.write(decompressed_text)
