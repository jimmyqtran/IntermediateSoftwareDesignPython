"""
CS3B, Assignment #10, Online Dictionary
Jimmy Tran
Testing
"""

import unittest
from OnlineDictionary import *


class TimeFuncTest(unittest.TestCase):
    def testTimeFunc1(self):
        result, duration = time_func(pow, 2, 128)
        self.assertEqual(result, 340282366920938463463374607431768211456)
        self.assertTrue(isinstance(duration, float))

    def testTimeFunc2(self):
        result, duration = time_func((lambda a, b: a - b), a=2, b=5)
        self.assertEqual(result, -3)
        self.assertTrue(isinstance(duration, float))

        result, duration = time_func((lambda a, b: a - b), b=2, a=5)
        self.assertEqual(result, 3)
        self.assertTrue(isinstance(duration, float))

        result, duration = time_func((lambda a, b: a - b), 2, 5)
        self.assertEqual(result, -3)
        self.assertTrue(isinstance(duration, float))

        result, duration = time_func((lambda a, b: a - b), 2, b=5)
        self.assertEqual(result, -3)
        self.assertTrue(isinstance(duration, float))

    def setUp(self):
        self.dictionary = Dictionary(source=DictionarySource.OXFORD_ONLINE)

    def testTimeFuncDictionary(self):
        word = "ace"

        # ONLINE
        entry, source, duration = self.dictionary.search(word)
        self.assertTrue(isinstance(entry, DictionaryEntry))
        self.assertEqual(word, entry.word)
        self.assertEqual("noun", entry.part_of_speech)
        self.assertEqual("a playing card with a single spot on it, "
                         "ranked as the highest card in its suit in most card games",
                         entry.definition)
        self.assertEqual("the ace of diamonds", entry.example)
        self.assertEqual(DictionarySource.OXFORD_ONLINE, source)
        self.assertTrue(isinstance(duration, float))


        # CACHE
        entry2, source2, duration2 = self.dictionary.search(word)
        self.assertTrue(isinstance(entry2, DictionaryEntry))
        self.assertEqual(word, entry2.word)
        self.assertEqual("noun", entry2.part_of_speech)
        self.assertEqual("a playing card with a single spot on it, "
                         "ranked as the highest card in its suit in most card games",
                         entry2.definition)
        self.assertEqual("the ace of diamonds", entry2.example)
        self.assertEqual(DictionarySource.CACHE, source2)
        self.assertTrue(isinstance(duration2, float))
        # Check that the second duration is faster than the first duration
        self.assertLess(duration2, duration)

        word = "python"

        # ONLINE AGAIN
        entry, source, duration = self.dictionary.search(word)
        self.assertTrue(isinstance(entry, DictionaryEntry))
        self.assertEqual(word, entry.word)
        self.assertEqual("noun", entry.part_of_speech)
        self.assertEqual("a large heavy-bodied nonvenomous snake occurring throughout the Old World tropics, "
                         "killing prey by constriction and asphyxiation.",
                         entry.definition)
        self.assertEqual(None, entry.example)
        self.assertEqual(DictionarySource.OXFORD_ONLINE, source)
        self.assertTrue(isinstance(duration, float))

        # CACHE AGAIN
        entry2, source2, duration2 = self.dictionary.search(word)
        self.assertTrue(isinstance(entry2, DictionaryEntry))
        self.assertEqual(word, entry2.word)
        self.assertEqual("noun", entry2.part_of_speech)
        self.assertEqual("a large heavy-bodied nonvenomous snake occurring throughout the Old World tropics, "
                         "killing prey by constriction and asphyxiation.",
                         entry2.definition)
        self.assertEqual(None, entry2.example)
        self.assertEqual(DictionarySource.CACHE, source2)
        self.assertTrue(isinstance(duration2, float))
        # Check that the second duration is faster than the first duration
        self.assertLess(duration2, duration)

