import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from runtime_windows.audio_player.audio_queue_player import AudioItem, AudioQueue


def test_queue_enqueue_and_next():
    queue = AudioQueue()
    queue.enqueue(AudioItem(path="a.wav"))
    item = queue.next_item()
    assert item is not None
    assert item.path == "a.wav"
    assert queue.next_item() is None


def test_queue_stop_clears():
    queue = AudioQueue()
    queue.enqueue(AudioItem(path="a.wav"))
    queue.next_item()
    queue.stop()
    assert queue.current is None
    assert queue.queue == []


def test_queue_replay():
    queue = AudioQueue()
    queue.enqueue(AudioItem(path="a.wav"))
    queue.next_item()
    replayed = queue.replay()
    assert replayed is not None
    assert replayed.path == "a.wav"
