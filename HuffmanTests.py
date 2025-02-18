from GenerateMegaTextFile import deserializeAverageCode
from HuffmanCoding import runCompression
##Testing and debugging

#Display results of Huffman coding - compare two encodings for a particular text file
def compareBitStats(labels: list[str], *referenceBitsDescending):
    referenceBitsList = list(referenceBitsDescending)
    for i in range(0, len(referenceBitsList)):
        print(labels[i] + ": " + str(referenceBitsList[i]))
    print(f"Most optimal percentage saved (with {labels[-1]}): {str(round((referenceBitsList[0] - referenceBitsList[-1])/referenceBitsList[0] * 100, 2))}%")
    print(f"Min bit-length encoding v. {labels[-1]} percentage saved: {str(round((referenceBitsList[1] - referenceBitsList[-1])/referenceBitsList[1] * 100, 2))}%")
    print("")

TEXT_PATH = "Roosevelt_History.txt"

codeAverage = deserializeAverageCode()

#Compute space of all encodings
asciiBitsEncoding, huffmanBitsEncoding = runCompression(TEXT_PATH, minFixedBits = False)
minBitsEncoding, _ = runCompression(TEXT_PATH, minFixedBits = True)
_, huffmanBitsAverage = runCompression(TEXT_PATH, code = codeAverage, minFixedBits = True)

#Compare all methods of encoding
compareBitStats(["8-bit encoding", "Minimum bit-length encoding", "Huffman (average) encoding", "Huffman (text-specific) encoded"], asciiBitsEncoding, minBitsEncoding, huffmanBitsAverage, huffmanBitsEncoding)

#Compare with alternate text Huffman code
TEXT_PATH_OTHER = "MurderInTheMaze.txt"
minBitsEncodingOther, huffmanBitsEncodingOther, codeOther = runCompression(TEXT_PATH_OTHER, minFixedBits=True, returnCode=True)
_, huffmanBitsEncodingOtherRoosevelt = runCompression(TEXT_PATH, code=codeOther, minFixedBits=True)
print(f"Huffman (alternate-text-encoded): {huffmanBitsEncodingOtherRoosevelt}")
print(f"Min bit-length encoding v. Huffman (alternate-text-encoded) space saved: {(round((minBitsEncoding-huffmanBitsEncodingOtherRoosevelt)/minBitsEncoding*100, 2))}%")
print(f"Min bit-length encoding v. Huffman (average) space saved: {(round((minBitsEncoding-huffmanBitsAverage)/minBitsEncoding*100, 2))}%")

