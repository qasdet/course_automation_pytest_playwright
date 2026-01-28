import pytest
import tempfile

@pytest.fixture
def temp_file():
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"hello")
    f.flush()
    f.close()
    yield f.name

    # cleanup
    try:
        import os
        os.remove(f.name)
    except Exception:
        pass
