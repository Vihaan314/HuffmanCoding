from collections import Counter
from dataclasses import dataclass, field
from typing import Optional, Dict
from queue import PriorityQueue
import math

from GenerateMegaTextFile import deserializeAverageCode, serializeAverageCode, generateMegaText

#Main average code generation (is run once to create serialized average code)
def generateAverageCode():
    MEGA_TEXT_PATH = "mega_text.txt"
    
    #Generate mega text file
    generateMegaText()
    
    #Generate the average code from mega text and save
    _, _, codeMega = runCompression(MEGA_TEXT_PATH)
    serializeAverageCode(codeMega)
    

#Python dataclass automatically creates biolerplate code for fields
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
    return count
    
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

def computeMinBitLength(text):
    #Is just ceiling of log_2(#distinct characters)
    charCount = len(set(text))
    return math.ceil(math.log2(charCount))

#Main running code
def runCompression(path, code = None, minFixedBits = False, returnCode = False):
    codeGiven = bool(code) #None means false -> no code given
    
    text = readBook(path)
    
    #If code is not given, create it with Huffman coding
    if not codeGiven:
        freqs = countLetterFrequencies(text)
        code = createCodeMap(freqs)
        
    textBits = 0
    #If fixed bit return is needed, compute minimum fixed bit length and multiply by number of characters, else blocks of 8
    if minFixedBits:
        minBitLength = computeMinBitLength(text)
        textBits = len(text) * minBitLength
    else:
        textBits = len(text)*8

    #Encode text with code
    huffmanCompressed = "".join(code[char] for char in text if char in code)
    huffmanBits = len(huffmanCompressed) 

    return (textBits, huffmanBits, code) if returnCode else (textBits, huffmanBits)




