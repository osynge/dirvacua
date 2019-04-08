import pydirvacua.dirvacua


def test_split_line_by_delimiter_with_regdelexp():
    testdata = [
        ('1-2-3-4', ['1', '-', '2', '-', '3', '-', '4']),
        ('1_2_3_4', ['1', '_', '2', '_', '3', '_', '4']),
        ('1.2.3.4', ['1', '.', '2', '.', '3', '.', '4']),
        ('1,2,3,4', ['1', ',', '2', ',', '3', ',', '4']),
        ('1/2/3/4', ['1', '/', '2', '/', '3', '/', '4']),
        ]
    for data, expected in testdata:
        result = pydirvacua.dirvacua.split_line_by_delimiter(data, pydirvacua.dirvacua.regdelexp)
        assert (result == expected)
