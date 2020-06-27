"""
Local Dictionary
Jimmy Tran
"""

from datalist import *
from enum import Enum
import json


class DictionaryEntry:
    def __init__(self, word, part_of_speech, definition, example=None):
        self.word = word
        self.part_of_speech = part_of_speech
        self.definition = definition
        self.example = example

    def __str__(self):
        return f"Word          : {self.word} \n" \
               f"Part of speech: {self.part_of_speech} \n" \
               f"Definition    : {self.definition} \n" \
               f"Example       : {self.example}"


class LocalDictionary:
    def __init__(self, dictionary_json_name="dictionary.json"):
        self.dictionary = {}
        filename = dictionary_json_name
        with open(filename) as json_file:
            data = json.load(json_file, object_hook=self.my_decoder)
            for entry in data:
                self.dictionary[entry.word] = entry

    @staticmethod
    def my_decoder(thingy):
        if "entries" in thingy:
            mega_list = []
            d = thingy["entries"]
            for entry in d:
                a = DictionaryEntry(entry["word"], entry["part_of_speech"], entry["definition"])
                if "example" in entry:
                    a.example = entry["example"]
                mega_list.append(a)

            return mega_list
        return thingy

    def search(self, word):
        if word not in self.dictionary:
            raise KeyError("The word is not in the dictionary.")
        return self.dictionary[word]

    def __str__(self):
        print()


class DictionaryEntryCache(DataList):
    def __init__(self, capacity=10):
        super().__init__()
        if capacity < 1:
            raise ValueError("There must be at least a capacity of one")
        self.capacity = capacity

    def add(self, entry):
        if not isinstance(entry, DictionaryEntry):
            raise TypeError("The entry should be of type Dictionary Entry")
        count = 0
        self.reset_current()
        while self.current is not None:
            self.iterate()
            count += 1
        self.reset_current()
        if count >= self.capacity:
            for _ in range(self.capacity - 1):
                self.iterate()
            self.current.next = None
        self.add_to_head(entry)

    def search(self, word):
        self.reset_current()
        while True:
            node = self.iterate()
            if not node:
                raise KeyError("Word not in here")
            elif node.data.word == word:
                temp = node.data
                self.remove(node.data)
                self.add(temp)
                self.reset_current()
                return self.head.next


class DictionarySource(Enum):
    LOCAL = 0
    CACHE = 1


class Dictionary:
    def __init__(self):
        self.local = LocalDictionary()
        self.cache = DictionaryEntryCache()

    def search(self, word):
        try:
            return self.cache.search(word), DictionarySource.CACHE
        except:
            if word not in self.local.dictionary:
                raise KeyError("Word is not in here")
            self.cache.add(self.local.dictionary[word])
            return self.local.search(word), DictionarySource.LOCAL

if __name__ == '__main__':
    big_dict = Dictionary()
    while True:
        try:
            wordy = input("Enter a word to lookup: ")
            actual_entry = big_dict.search(wordy)
            print(actual_entry[0])
            print(f"(Found in {actual_entry[1].name})")
        except KeyError as e:
            print(f"{e}: {wordy}")
            continue
