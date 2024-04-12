import re

class PorterStemmer:
    def __init__(self):
        self.vowels = 'aeiou'
        self.consonants = 'bcdfghjklmnpqrstvwxyz'
        self.m = 0

    def is_consonant(self, word, index):
        return word[index] in self.consonants

    def is_vowel(self, word, index):
        return word[index] in self.vowels

    def get_measure(self, word):
        measure = 0
        for i in range(len(word)):
            if self.is_consonant(word, i):
                if i != 0 and self.is_vowel(word, i-1):
                    measure += 1
        return measure

    def ends_double_consonant(self, word):
        return len(word) >= 2 and word[-1] == word[-2] and self.is_consonant(word, -1)

    def ends_cvc(self, word):
        if len(word) >= 3:
            if self.is_consonant(word, -1) and self.is_vowel(word, -2) and self.is_consonant(word, -3):
                if word[-1] not in 'wxz':
                    return True
        return False

    def replace_suffix(self, word, suffix, replacement):
        return re.sub(suffix + "$", replacement, word)

    def step1a(self, word):
        if word.endswith('sses'):
            return self.replace_suffix(word, 'sses', 'ss')
        elif word.endswith('ies'):
            return self.replace_suffix(word, 'ies', 'i')
        elif word.endswith('ss'):
            return word
        elif word.endswith('s'):
            return self.replace_suffix(word, 's', '')
        return word

    def step1b(self, word):
        if word.endswith('eed'):
            if self.get_measure(word[:-3]) > 0:
                return self.replace_suffix(word, 'eed', 'ee')
            else:
                return word
        elif 'ed' in word:
            if any(word.endswith(suffix) for suffix in ['at', 'bl', 'iz']):
                return word[:-1]
            elif self.ends_double_consonant(word) and not any(word.endswith(suffix) for suffix in ['l', 's', 'z']):
                return word[:-1]
            elif self.get_measure(word[:-2]) == 1 and self.ends_cvc(word[:-2]):
                return word[:-1]
        elif 'ing' in word:
            if any(word.endswith(suffix) for suffix in ['at', 'bl', 'iz']):
                return word[:-1]
            elif self.ends_double_consonant(word) and not any(word.endswith(suffix) for suffix in ['l', 's', 'z']):
                return word[:-1]
            elif self.get_measure(word[:-3]) == 1 and self.ends_cvc(word[:-3]):
                return word[:-1]
        return word

    def step1c(self, word):
        if word.endswith('y') and self.get_measure(word) > 0:
            return self.replace_suffix(word, 'y', 'i')
        return word

    def step2(self, word):
        step2_replacements = {
            'ational': 'ate',
            'tional': 'tion',
            'enci': 'ence',
            'anci': 'ance',
            'izer': 'ize',
            'abli': 'able',
            'alli': 'al',
            'entli': 'ent',
            'eli': 'e',
            'ousli': 'ous',
            'ization': 'ize',
            'ation': 'ate',
            'ator': 'ate',
            'alism': 'al',
            'iveness': 'ive',
            'fulness': 'ful',
            'ousness': 'ous',
            'aliti': 'al',
            'iviti': 'ive',
            'biliti': 'ble',
        }
        for suffix, replacement in step2_replacements.items():
            if word.endswith(suffix):
                if self.get_measure(word[:-len(suffix)]) > 0:
                    return self.replace_suffix(word, suffix, replacement)
                else:
                    return word
        return word

    def step3(self, word):
        step3_replacements = {
            'icate': 'ic',
            'ative': '',
            'alize': 'al',
            'iciti': 'ic',
            'ical': 'ic',
            'ful': '',
            'ness': '',
        }
        for suffix, replacement in step3_replacements.items():
            if word.endswith(suffix):
                if self.get_measure(word[:-len(suffix)]) > 0:
                    return self.replace_suffix(word, suffix, replacement)
                else:
                    return word
        return word

    def step4(self, word):
        step4_replacements = {
            'al': '',
            'ance': '',
            'ence': '',
            'er': '',
            'ic': '',
            'able': '',
            'ible': '',
            'ant': '',
            'ement': '',
            'ment': '',
            'ent': '',
            'ou': '',
            'ism': '',
            'ate': '',
            'iti': '',
            'ous': '',
            'ive': '',
            'ize': '',
        }
        for suffix, replacement in step4_replacements.items():
            if word.endswith(suffix):
                if self.get_measure(word[:-len(suffix)]) > 1:
                    return self.replace_suffix(word, suffix, replacement)
                else:
                    return word
        if word.endswith('sion') or word.endswith('tion'):
            if self.get_measure(word[:-3]) > 1:
                return word[:-3]
        return word

    def step5a(self, word):
        if word.endswith('e'):
            if self.get_measure(word[:-1]) > 1:
                return word[:-1]
            elif self.get_measure(word[:-1]) == 1 and not self.ends_cvc(word[:-1]):
                return word[:-1]
        return word

    def step5b(self, word):
        if self.get_measure(word) > 1 and self.ends_double_consonant(word) and word.endswith('l'):
            return word[:-1]
        return word

    def stem_word(self, word):
        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word

    def stem(self, text):
        stemmed_text = [self.stem_word(word) for word in text.split()]
        return ' '.join(stemmed_text)