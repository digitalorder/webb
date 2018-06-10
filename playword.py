from playtime_data import PlaytimeData
from word import Word
from longterm_data import LongtermData
import copy


class PlayWord(Word, PlaytimeData, LongtermData):
    def __init__(self, word, longterm_data):
        Word.__init__(self, word.german, word.german_gender, word.native, word.id_num)
        PlaytimeData.__init__(self)
        LongtermData.__init__(self, word.id_num, longterm_data.success_timestamps, longterm_data.failures_timestamps)

    def __repr__(self):
        as_word = copy.deepcopy(self)
        as_word.__class__ = Word
        as_longterm_data = copy.deepcopy(self)
        as_longterm_data.__class__ = LongtermData
        as_playtime_data = copy.deepcopy(self)
        as_playtime_data.__class__ = PlaytimeData
        return "PlayWord('{}' learned {}, current playtime {})".format(repr(as_word), repr(as_longterm_data),
                                                                       repr(as_playtime_data))

