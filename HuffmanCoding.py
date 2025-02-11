from collections import Counter
from dataclasses import dataclass, field
from typing import Optional, Dict
from queue import PriorityQueue
from itertools import islice

from GenerateMegaTextFile import deserializeAverageCode, serializeAverageCode, generateMegaText

#Dataclass automatically creates biolerplate code for fields
@dataclass(order=True)
class TreeVertex:
    weight: int
    c: Optional[str] = field(compare=False, default=None)  
    leftChild: Optional['TreeVertex'] = field(compare=False, default=None)
    rightChild: Optional['TreeVertex'] = field(compare=False, default=None)

    
def readBook(path):
    f = open(path, "r", encoding="utf8")
    return f.read() 

def countLetterFrequencies(text):    
    #Create dictionary of characters to their frequencies
    count = dict(Counter(text))
    if len(count) > 500:
        print(str(dict(islice(dict(sorted(count.items(), key=lambda x: x[1], reverse=True)).items(), 500))) + "\n")
    else:
        print(str(dict(sorted(count.items(), key=lambda x: x[1], reverse=True))) + "\n")
    return (count)
    
def buildTree(freqs):
    pq = PriorityQueue()

    #Create priority queue with character nodes
    for char in freqs:
        node = TreeVertex(weight = freqs[char], c = char)
        pq.put(node)        

    #While more parent nodes can be created
    while (pq.qsize() > 1):
        leftNode = pq.get()
        rightNode = pq.get()
        
        #Create parent node with combined weight of children
        combinedWeight = leftNode.weight + rightNode.weight
        parentNode = TreeVertex(weight = combinedWeight, leftChild = leftNode, rightChild = rightNode)
        
        #Add to queue
        pq.put(parentNode)

    #No more parent nodes can be created -> we are left with the root node
    return pq.get()


def createCodeMap(freqs):
    root = buildTree(freqs)
    huffmanCode = {}

    #Traverse Huffman tree to create code map
    def traverseTree(node: TreeVertex, currentCode: str):        
        #If node has associated character
        if node.c:
            huffmanCode[node.c] = currentCode
            return

        #If no character, recursively:
        #Traverse left child and add '0' to current code
        traverseTree(node.leftChild, currentCode + "0")
        
        #Traverse right child and add '1' to the current code
        traverseTree(node.rightChild, currentCode + "1")

    #Traverse tree and create map from root node
    traverseTree(root, "")
    return huffmanCode


#Main running code
def runCompression(path, code = None):
    codeGiven = bool(code) #None means false -> no code given
    
    text = readBook(path)
    
    #If code is not given, create it with Huffman coding
    if not codeGiven:
        freqs = countLetterFrequencies(text)
        code = createCodeMap(freqs)

    if len(code) > 500:
        print(str(dict(islice(code.items(), 500))) + "\n")
    else:
        print(str(code) + "\n")
        
    #Fixed bits is just 
    fixedBits = len(text) * 8

    #Encode text with code
    huffmanCompressed = "".join(code[char] for char in text if char in code)
    huffmanBits = len(huffmanCompressed) 

    if not codeGiven:
        return fixedBits, huffmanBits, code
    return fixedBits, huffmanBits

#Display results of Huffman coding
def displayHuffmanStats(fixedBits, huffmanBits):
    print("Fixed-length encded: " + str(fixedBits))
    print("Huffman encoded: " + str(huffmanBits))
    #Calculate difference of fixed length and huffman encoded
    print("Bits saved: " + str(fixedBits - huffmanBits))
    print("")


#Main average code generation (is run once)
def generateAverageCode():
    MEGA_TEXT_PATH = "mega_text.txt"
    
    #Generate mega text file
##    generateMegaText()
    
    #Generate the average code from mega text and save
    _, _, codeMega = runCompression(MEGA_TEXT_PATH)
    serializeAverageCode(codeMega)

##generateAverageCode()

#Test path for text
TEXT_PATH = "Roosevelt_History.txt"

#Test 1: Text-specific encoding
fixedBitsRegular, huffmanBitsRegular, codeRegular = runCompression(TEXT_PATH)
displayHuffmanStats(fixedBitsRegular, huffmanBitsRegular)

#Test 2: Average encoding
codeAverage = deserializeAverageCode()
fixedBitsAverage, huffmanBitsAverage = runCompression(TEXT_PATH, code = codeAverage)
displayHuffmanStats(fixedBitsAverage, huffmanBitsAverage)





