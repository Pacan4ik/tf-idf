from collections import Counter


class Lexicon:
    def __init__(self, words: []):
        self.len_total = len(words)
        self.counter = Counter(words)
        self._items = list(self.counter.items())

    def items(self):
        return self._items

    def __getitem__(self, key):
        if key in self.counter:
            return self.counter[key], self.counter[key] / self.len_total
        else:
            raise KeyError(f"Word '{key}' not found in the text")

    def __setitem__(self, key, value):
        raise NotImplementedError("Setting items is not supported")

    def __delitem__(self, key):
        raise NotImplementedError("Deleting items is not supported")

    def __contains__(self, key):
        return key in self.counter

    def __len__(self):
        return len(self.counter)

    # WARN!!! every calling str calls dividing loop
    def __str__(self):
        return "{" + ", ".join(
            [f"'{word}': ({count}, {count / self.len_total})" for word, count in self.counter.items()]) + "}"

    def __repr__(self):
        return f"Lexicon(len_total={self.len_total!r}, counter={repr(dict(self.counter))!r})"

    def __iter__(self):
        self._iter_index = 0
        self._keys = list(self.counter.keys())
        return self

    def __next__(self):
        if self._iter_index < len(self.counter):
            word, count = self._items[self._iter_index]
            self._iter_index += 1
            return word, (count, count / self.len_total)
        else:
            raise StopIteration
