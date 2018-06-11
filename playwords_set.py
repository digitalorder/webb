from datetime import datetime
from playword import PlayWord
import json
from word import Word
from longterm_data import LongtermData


class PlaywordsSet:
    def __init__(self, words_file, longterm_data_file=None):
        with open(words_file, 'r') as f:
            words = PlaywordsSet._load_words(f)

        if longterm_data_file:
            try:
                with open(longterm_data_file, 'r') as f:
                    longterm_data = PlaywordsSet._load_progress(f)
            except FileNotFoundError:
                longterm_data = []
        else:
            longterm_data_file = "player_data.json"

        self._longterm_data_file = longterm_data_file

        self._words = list()
        for w in words:
            word_longterm_data = [d for d in longterm_data if d.id_num == w.id_num]
            if len(word_longterm_data) == 0:
                word_longterm_data = [LongtermData(w.id_num)]
            self._words.append(PlayWord(w, word_longterm_data[0]))

    @staticmethod
    def _load_words(f):
        plain_data = json.load(f)
        result = []
        for w in plain_data:
            result.append(Word.from_json(w))
        return result

    @staticmethod
    def _load_progress(f):
        plain_data = json.load(f)
        result = list()
        for d in plain_data:
            try:
                result.append(LongtermData.from_json(d))
            except KeyError:
                continue
        return result

    def save_progress(self):
        with open(self._longterm_data_file, 'w') as f:
            json_repr = []
            for w in self._words:
                json_repr.append(w.to_json())
            json_words = json.dumps(json_repr, indent=4, sort_keys=True)
            f.write(json_words)

    def select_for_next_round(self):
        # 1. word wasn't remembered in this session
        filtered_playwords = [w for w in self._words if not w.learned_in_session]
        # 2. learned less then an minute ago
        filtered_playwords = [w for w in filtered_playwords if w.last_learned() > 600]
        return filtered_playwords

    def check_guess(self, word, response, again=False):
        if not again:
            word.attempts += 1

        if word.german_gender == response:
            word.success_in_row += 1
            result = True
        else:
            result = False
            word.success_in_row = 0
            if not again:
                word.failures_timestamps.append(datetime.now())

        if word.success_in_row == 3:
            word.learned_in_session = True
            word.success_timestamps.append(datetime.now())
        return result
