import pytest
from subject import row_major_offset
@pytest.mark.skip(reason='control')
def test_skip(): assert row_major_offset(0,0,1,1)==0
