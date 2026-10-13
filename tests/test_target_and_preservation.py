import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import refresh_realtime_20261013 as refresh
from industry_colors import style_payload


class RefreshContract(unittest.TestCase):
    def test_default_target_is_new_sheet(self):
        self.assertEqual(refresh.feishu.SPREADSHEET, 'RVKmszaTRh2lWoteg8bcQSKCnIc')
        self.assertEqual(refresh.TARGET, 'Wc32bt')

    def test_industry_style_never_overwrites_personal_note_column(self):
        values = [refresh.HEADERS, ['样本', '个人笔记', '电子', '半导体']]
        payload, _ = style_payload(
            values, refresh.TARGET,
            refresh.ROOT / 'config/industry_color_map_20261012.json',
            clear_to=3, l1_index=2, l2_index=3, column_count=17,
            excluded_columns={2},
        )
        ranges = [r for item in payload for r in item['ranges']]
        self.assertTrue(ranges)
        self.assertFalse(any(r.split('!')[1].startswith('B') for r in ranges))
        self.assertIn('Wc32bt!A2:A2', ranges)
        self.assertIn('Wc32bt!Q2:Q2', ranges)


if __name__ == '__main__':
    unittest.main()
