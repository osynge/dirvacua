import os
import logging


class TestModule_runnershell2:
    def test_initialise(self):
        pass


if __name__ == "__main__":
    logging.basicConfig()
    LoggingLevel = logging.WARNING
    logging.basicConfig(level=LoggingLevel)
    log = logging.getLogger("main")
    new_path = os.path.dirname(__file__)
    import pytest
    pytest.main(['-x', new_path])
