from datetime import datetime


class LongtermData:
    def __init__(self, word_id_num, success_timestamps=None,
                 failures_timestamps=None):
        if success_timestamps is None:
            self._success_timestamps = list()
        else:
            self._success_timestamps = success_timestamps
        if failures_timestamps is None:
            self._failures_timestamps = list()
        else:
            self._failures_timestamps = failures_timestamps
        self._id_num = word_id_num

    @property
    def success_timestamps(self):
        return self._success_timestamps

    @success_timestamps.setter
    def success_timestamps(self, value):
        self._success_timestamps = value

    @property
    def failures_timestamps(self):
        return self._failures_timestamps

    @property
    def id_num(self):
        return self._id_num

    def to_json(self):
        result = dict()
        result["id_num"] = self._id_num
        result["success_timestamps"] = [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in self._success_timestamps]
        result["failures_timestamps"] = [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in self._failures_timestamps]
        return result

    @staticmethod
    def from_json(d):
        id_num = d['id_num']
        success_timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in d['success_timestamps']]
        failures_timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in d['failures_timestamps']]
        return LongtermData(word_id_num=id_num, success_timestamps=success_timestamps,
                            failures_timestamps=failures_timestamps)

    def last_learned(self):
        if len(self._success_timestamps) == 0:
            last_ts = datetime.fromtimestamp(0)
        else:
            last_ts = self._success_timestamps[-1]

        diff = datetime.now() - last_ts
        return int(round(diff.total_seconds() / 60))

    def __repr__(self):
        if len(self._success_timestamps) == 0:
            return "never"
        
        text_repr = []
        for ts in self._success_timestamps:
            td = datetime.now() - ts
            td = int(round(td.total_seconds() / 60))
            if td < 1:
                text_repr.append("less than minute ago")
            elif td == 1:
                text_repr.append("a minute ago")
            elif td < 60:
                text_repr.append("{} minutes ago")
            else:
                td = td / 60
                if td == 1:
                    text_repr.append("an hour ago")
                elif td < 24:
                    text_repr.append("{} hours ago")
                else:
                    td = td / 24
                    if td == 1:
                        text_repr.append("a day ago")
                    else:
                        text_repr.append("{} days ago")

        result = "last time {} ({})".format(text_repr[-1], self._success_timestamps[-1].strftime("%Y-%m-%d %H:%M:%S"))

        if len(self._success_timestamps) > 1:
            result += "other timestamps: "
            for tr, ts in zip(text_repr[1:], self._success_timestamps[1:]):
                result += "{} ({}); ".format(tr, ts.strftime("%Y-%m-%d %H:%M:%S"))
        return result
