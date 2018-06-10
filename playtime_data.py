class PlaytimeData:
    def __init__(self):
        self._attempts = 0
        self._success_in_row = 0
        self._last_time_asked = 0
        self._learned_in_session = False

    @property
    def attempts(self):
        return self._attempts

    @attempts.setter
    def attempts(self, value):
        self._attempts = value

    @property
    def success_in_row(self):
        return self._success_in_row

    @success_in_row.setter
    def success_in_row(self, value):
        self._success_in_row = value

    @property
    def learned_in_session(self):
        return self._learned_in_session

    @learned_in_session.setter
    def learned_in_session(self, value):
        self._learned_in_session = value

    def __repr__(self):
        return "attempts {}, successes = {}".format(self._attempts, self._success_in_row)
