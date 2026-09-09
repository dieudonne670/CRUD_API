import types

from app import livestream


class DummyDB:
    def __init__(self):
        self.commits = 0

    def commit(self):
        self.commits += 1

    def refresh(self, obj):
        return None


def test_increment_viewers_updates_peak_and_current():
    stream = types.SimpleNamespace(current_viewers=2, peak_viewers=2)
    db = DummyDB()

    updated_stream = livestream.increment_viewers(db, stream)

    assert updated_stream.current_viewers == 3
    assert updated_stream.peak_viewers == 3
    assert db.commits == 1


def test_decrement_viewers_does_not_go_negative():
    stream = types.SimpleNamespace(current_viewers=0, peak_viewers=0)
    db = DummyDB()

    updated_stream = livestream.decrement_viewers(db, stream)

    assert updated_stream.current_viewers == 0
    assert db.commits == 1
