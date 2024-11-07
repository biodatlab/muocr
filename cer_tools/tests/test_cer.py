##############################################################################
# A unittest for cer.py
##############################################################################

import unittest
from cer_tools import cer
import pandas as pd

class TestCer(unittest.TestCase):
    
    def test_cer(self):
        # Test for same text
        cer_score = cer.cer(['hello', 'world'], ['hello', 'world'])
        self.assertEqual(cer_score, 0.0)
        cer_score = cer.cer(['เลขที่ 64 หมู่ 14 ถนนพหลโยธิน ตำบลปากน้ำโพ อำเภอเมือง จังหวัดนครสวรรค์ 60000', 'เลขที่ 62 หมู่ 12 ถนนพหลโยธิน ตำบลเวียง อำเภอเมือง จังหวัดเชียงราย 57000'], ['เลขที่ 64 หมู่ 14 ถนนพหลโยธิน ตำบลปากน้ำโพ อำเภอเมือง จังหวัดนครสวรรค์ 60000', 'เลขที่ 62 หมู่ 12 ถนนพหลโยธิน ตำบลเวียง อำเภอเมือง จังหวัดเชียงราย 57000'])
        self.assertEqual(cer_score, 0.0)
        # Test for different text
        cer_score = cer.cer(['abcd', 'efgh'], ['dcab', 'hgfe'])
        self.assertEqual(cer_score, 1.0)
        cer_score = cer.cer(['เลขที่ 84 หมู่ 14 ถนนพหลโยธิน ตำบลปากน้ำโพ อำเภอเมือง จังหวัดนครสวรรค์ 60000', 'เลขที่ 62 หมู่ 12 ถนนพหลโยธิน ตำบลเวียง อำเภอเมือง จังหวัดเชียงราย 57000'], ['เลขที่ 64 หมู่ 14 ถนนพหลโยธิน ตำบลปากน้ำโพ อำเภอเมือง จังหวัดนครสวรรค์ 60000', 'เลขที่ 62 หมู่ 12 ถนนพหลโยธิน ตำบลเวียง อำเภอเมือง จังหวัดเชียงราย 57000'])
        assert cer_score > 0.0

    def test_read_file(self):
        df = cer.read_file('cer_tools/tests/test_data.csv')
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_column_to_list(self):
        df = cer.read_file('cer_tools/tests/test_data.csv')
        values = cer.get_column_to_list(df, 'groundtruths')
        self.assertEqual(values, ['hello', 'world'])
        values = cer.get_column_to_list(df, 'predictions')
        self.assertEqual(values, ['world', 'hello'])