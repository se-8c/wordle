import random
from typing import List


from models.user import charResult


class Node:

    def __init__(self, letter=None, end_word=False):
        self.letter = letter            # letter stored at this node
        self.end_word = end_word        # True if this letter is the end of a word
        self.left = None    # pointing to the left child Node, which holds a letter < self.letter
        self.middle = None  # pointing to the middle child Node
        self.right = None   # pointing to the right child Node, which holds a letter > self.letter

# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Ref: https://iq.opengenus.org/autocomplete-with-ternary-search-tree/
# Ref: https://leetcode-cn.com/problems/implement-trie-prefix-tree/solution/ternary-search-triessan-cha-qian-zhui-shu-geng-hao/
# ------------------------------------------------------------------------

class TernarySearchTreeDictionary():

    def __init__(self) -> None:
        self.rootNode = None

    def build_dictionary(self, words: List[str]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for item in words:
            self.insertHelper(item)
        return True 


    def search(self, word: str) -> str:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        node = self.searchHelper(self.rootNode,word,0)
        if node is not None and node.end_word:
            return node.letter
        else:
            return None

    def add_word_frequency(self, word: str) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        # place holder for return
        search_result = self.search(word)
        if search_result == None:
            self.insertHelper(word)
            return True
        else:
            return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        search_result = self.deleteHelper(self.rootNode,word,0)
        if search_result is not None:
            return True
        else:
            return False

    def insertHelper(self, word: str) -> None:
        """
        insert a word and its frequency to the dictionary
        @param word: word to be inserted
        @param frequency: frequency of the word
        """
        self.rootNode = self.put(self.rootNode, word,0)


    def put(self, node: Node, word: str,index:int) -> None:
        """
        insert a word and its frequency to the dictionary
        @param node: node to be inserted
        @param wf: WordFrequency to be inserted (word, frequency)
        @param d: depth of the node
        """
        char = word[index]
        if node is None:
            node = Node(letter=char)
        if char < node.letter:
            node.left = self.put(node.left, word, index)
        elif char > node.letter:
            node.right = self.put(node.right, word, index)
        elif index < len(word) - 1:
            node.middle = self.put(node.middle, word, index + 1)
        else:
            node.end_word = True
        return node

    def searchHelper(self,node :Node,word : str,index : int) -> Node:
        if node is None:
            return None
        if index == len(word) - 1 and node.letter == word[index]:
            return node
        if word[index] == node.letter:
            return self.searchHelper(node.middle,word,index + 1)
        if word[index] < node.letter:
            return self.searchHelper(node.left,word,index)
        if word[index] > node.letter:
            return self.searchHelper(node.right,word,index)


    def deleteHelper(self, node :Node,word : str,index : int) -> Node:
        """
        First the last node (here is p of cup) end_word change to False, 
        and then start from it back, encounter end_word is False is not 
        yet left / right node will be deleted, have left or / and right 
        son but no mid son on that it will be deleted itself to replace
        that son to their original position.
        @param node: node to be inserted
        @param wf: WordFrequency to be inserted (word, frequency)
        @param index: index of the word
        """
        if node is None:
            return None

        if index == len(word) - 1 and node.letter == word[index]:
            if node.end_word:
                return node
            return None

        if word[index] == node.letter:
            result = self.deleteHelper(node.middle,word,index + 1)
            if result is not None:
                self.nodeDelete(node,node.middle,word,index + 1)
        if word[index] < node.letter:
            result = self.deleteHelper(node.left,word,index)
            if result is not None:
                self.nodeDelete(node,node.left,word,index)
        if word[index] > node.letter:
            result = self.deleteHelper(node.right,word,index)
            if result is not None:
                self.nodeDelete(node,node.right,word,index)
        return result


    def nodeDelete(self,parent :Node,child:Node,word:str,index:int):
        if child is None:
            return None
        """
        the word is a prefix of another word then it can be deleted by simply setting the boolean field
        of the node storing the last letter to False
        For example, if (cut, 10) is to be deleted from the tree in Figure 1, then we only need to change
        the boolean field of the node storing 't' to False
        """
        """
        the word has some unique suffix, then we need to delete nodes corresponding to the suffix only. 
        For example, if (cup, 30) is to be removed, then only the node storing the last letter 'p' needs 
        to be deleted from the tree.
        """
        if word[index] == child.letter:
            if child.left is not None or child.right is not None or child.middle is not None:
                if index + 1 == len(word):
                    child.end_word = False
                return parent
            if child.left is None and child.right is None and child.middle is None:
                if parent.left == child:
                    parent.left = None
                elif parent.right == child:
                    parent.right = None
                elif parent.middle == child:
                    parent.middle = None
                return parent

wordsDict = TernarySearchTreeDictionary()
wordsArray = []
wordCount = 0


def getRandomWord() -> str:
    global wordCount
    return wordsArray[random.randint(0,wordCount - 1)]

def load_words():
    f = open("words.txt")
    line = f.readline()
    while line:
        word = line.replace("\n", "")
        word = word.lower()
        wordsArray.append(word)
        line = f.readline()
    f.close()
    wordsDict.build_dictionary(wordsArray)

def isWord(word: str) -> bool:
    return wordsDict.search(word)


def isCorrect(input: str,word:str):
    '''
    return 
    code -3 is meaning the lenght of input is not equal to 5
    code -4 is meaning the input is not a word
    '''

    if len(input) != 5:
        # -3 is meaning the lenght of input is not equal to 5
        return -3,None
    if wordsDict.search(input) == None:
        # -4 is meaning the input is not a word
        return -4,None
    
    result = []
    for i in range(5):
        # code = -2 means the letter is not in the word
        # code = -1 The word is in this letter but not in the correct position
        # code = 1 The word is in this letter and in the correct position
        if input[i] not in word:
            temp = charResult(letter= input[i],code= -2)
            result.append(temp.dict())
        else:
            if input[i] == word[i]:
                temp = charResult(letter= input[i],code= 1)
                result.append(temp.dict())
            else:
                temp = charResult(letter= input[i],code= -1)
                result.append(temp.dict())
    if input == word:
        return 2,result
    else:
        return 3,result


def dictTest():
    global wordCount
    wordCount = len(wordsArray)
    print("Total words: " + str(wordCount) + "\n")
    result = "True" if wordsDict.search("hello") is not None else "False"
    print("is hello in dictionary: " + result + "\n")
    result = "True" if wordsDict.search("nights") is not None else "False"
    print("is nights in dictionary: " +  result + "\n")
    print("random word: " + getRandomWord() + "\n")