"""
Local Dictionary
Jimmy Tran
Unit Testing
"""
import itertools
import json
import unittest
from LocalDictionary import *

class DictionaryEntryTestCase(unittest.TestCase):
    pass

class LocalDictionaryTestCase(unittest.TestCase):
    def testLocalDictionary(self):
        local_dict = LocalDictionary()
        self.assertIsInstance(local_dict, LocalDictionary)

    def testSearch(self):
        local_dict = LocalDictionary()
        self.assertIsInstance(local_dict.search("fly"), DictionaryEntry)
        self.assertEqual(local_dict.search("fly").word, "fly")
        self.assertEqual(local_dict.search("fly").part_of_speech, "verb")
        self.assertEqual(local_dict.search("python").word, "python")
        self.assertEqual(local_dict.search("python").example, None)
        self.assertEqual(local_dict.search("jolly").definition, "full of high spirits")
        self.assertRaises(KeyError, lambda: local_dict.search("potato"))

class DictionaryEntryCacheTestCase(unittest.TestCase):
    def testAdd(self):
        local_dict = LocalDictionary()
        #instantiate a DictionaryEntryCache of capacity 3
        cache = DictionaryEntryCache(capacity=3)

        cache.add(local_dict.search("fly"))
        self.assertEqual(cache.head.next.data.word, "fly")
        self.assertEqual(cache.head.next.next, None)

        cache.add(local_dict.search("foothill"))
        self.assertEqual(cache.head.next.data.word, "foothill")
        self.assertEqual(cache.head.next.next.data.word, "fly")
        self.assertEqual(cache.head.next.next.next, None)

        cache.add(local_dict.search("python"))
        self.assertEqual(cache.head.next.data.word, "python")
        self.assertEqual(cache.head.next.next.data.word, "foothill")
        self.assertEqual(cache.head.next.next.next.data.word, "fly")
        self.assertEqual(cache.head.next.next.next.next, None)

        cache.add(local_dict.search("jolly"))
        self.assertEqual(cache.head.next.data.word, "jolly")
        self.assertEqual(cache.head.next.next.data.word, "python")
        self.assertEqual(cache.head.next.next.next.data.word, "foothill")
        self.assertEqual(cache.head.next.next.next.next, None)


    def testSearch(self):
        # search when the word already exists in the cache
        local_dict = LocalDictionary()
        cache = DictionaryEntryCache(capacity=3)
        cache.add(local_dict.search("python"))
        cache.add(local_dict.search("foothill"))
        cache.add(local_dict.search("jolly"))
        cache.search("foothill")
        self.assertEqual(cache.head.next.data.word, "foothill")
        self.assertEqual(cache.head.next.next.data.word, "jolly")
        self.assertEqual(cache.head.next.next.next.data.word, "python")
        self.assertEqual(cache.head.next.next.next.next, None)

        # search when the word does not exist in the cache
        self.assertRaises(KeyError, lambda: cache.search("potato"))

        # search when the word is already in the cache but it's the only word
        cache2 = DictionaryEntryCache(capacity=3)
        cache2.add(local_dict.search("foothill"))
        cache2.search("foothill")
        self.assertEqual(cache2.head.next.data.word, "foothill")




class DictionaryTestCase(unittest.TestCase):
    def testDictionary(self):
        big_dict = Dictionary()
        wow = big_dict.search("foothill")
        self.assertEqual(wow[0].word, "foothill")
        self.assertEqual(wow[1], DictionarySource.LOCAL)
        wow_the_second_coming = big_dict.search("foothill")
        self.assertEqual(wow_the_second_coming[0].data.word, "foothill")
        self.assertEqual(wow_the_second_coming[1], DictionarySource.CACHE)
