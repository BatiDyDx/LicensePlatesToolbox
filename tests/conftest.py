import sys
import pytest


@pytest.fixture(scope="function")
def capture_stdout(monkeypatch):
    buffer = []

    def write_buffer(string: str) -> None:
        buffer.append(string)

    monkeypatch.setattr(sys.stdout, "write", write_buffer)
    return buffer
