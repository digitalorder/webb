class Word:
    def __init__(self, german, german_gender, native, id_num):
        self._german = german
        self._native = native
        self._german_gender = german_gender
        self._id_num = id_num

    @property
    def id_num(self):
        return self._id_num

    @property
    def german(self):
        return self._german

    @property
    def german_gender(self):
        return self._german_gender

    @property
    def native(self):
        return self._native

    @staticmethod
    def from_json(json_repr):
        return Word(json_repr['german'], json_repr['german_gender'], json_repr['native'], json_repr['id_num'])

    def __repr__(self):
        if self._german_gender == "masculine":
            gender = "der"
        elif self._german_gender == "feminine":
            gender = "die"
        elif self._german_gender == "neuter":
            gender = "das"
        else:
            gender = "?"

        return "{} {} / {}".format(gender, self._german, self._native)
