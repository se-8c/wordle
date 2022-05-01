from pickle import TRUE
import unittest

from utils import words
from app.routers import RespHelper
from app.routers import games


class TestRespHelper(unittest.TestCase):
    def test_resp_ok_code(self):
        result = RespHelper.resp_ok_code(1,1)
        self.assertEqual(result["code"],1)

    def test_resp_ok_code(self):
        result = RespHelper.resp_ok(1)
        self.assertEqual(result["data"],1)

    def test_resp_err(self):
        result = RespHelper.resp_err(-1,"error")
        self.assertEqual(result["code"],-1)
        self.assertEqual(result["msg"],"error")

class TestTernarySearchTreeDictionary(unittest.TestCase):

    def test_build_dictionary(self):
        words.load_words()
        self.assertEqual(words.wordsDict.build_dictionary(words.wordsArray), True) 

    def test_search_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.search("apple"), "e")

    def test_search_not_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.search("applee"), None)

    def test_add_word_frequency_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.add_word_frequency("appleef"), True)

    def test_add_word_frequency_not_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.add_word_frequency("apple"), False)

    def test_delete_word_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.delete_word("apple"), True)


    def test_delete_word_not_existWorld(self):
        words.load_words()
        words.wordsDict.build_dictionary(words.wordsArray)
        self.assertEqual(words.wordsDict.delete_word("applee"), False)

    def test_getRandomWord(self):
        words.load_words()
        words.wordCount = len(words.wordsArray)
        words.wordsDict.build_dictionary(words.wordsArray)
        world = words.getRandomWord()
        self.assertEqual(len(world),5)

    def test_load_words(self):
        words.load_words()
        self.assertGreater(len(words.wordsArray),0)

    def test_isWord(self):
        words.load_words()
        self.assertEqual(words.isWord("apple"),"e")

    def test_isWord_incorrect(self):
        words.load_words()
        self.assertEqual(words.isWord("applee"),None)

    def test_isCorrect_correct(self):
        words.load_words()
        result = words.isCorrect("apple","apple")
        self.assertEqual(result[0],2)

    def test_isCorrect_incorrect(self):
        words.load_words()
        result = words.isCorrect("applee","apple")
        self.assertEqual(result[0],-3)

    def test_isCorrect_input_isnot_word(self):
        words.load_words()
        result = words.isCorrect("aaaaa","apple")
        self.assertEqual(result[0],-4)

    def test_isCorrect_letter_notin_world(self):
        words.load_words()
        result = words.isCorrect("apple","table")
        self.assertEqual(result[1][1]["code"],-2)

    def test_isCorrect_letter_in_world(self):
        words.load_words()
        result = words.isCorrect("apple","table")
        self.assertEqual(result[1][0]["code"],-1)

    def test_isCorrect_letter_in_right_postion(self):
        words.load_words()
        result = words.isCorrect("apple","table")
        self.assertEqual(result[1][3]["code"],1)


