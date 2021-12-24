from huffman import HuffmanCoding


if __name__ == '__main__':
    h = HuffmanCoding()

    h.compress('data.txt', 'data.bin', 'data.pickle')

    h.decompress('data.bin', 'data_out.txt', 'data.pickle')
