import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from realtime_quotes import fetch_sina

class SinaQuotesTest(unittest.TestCase):
    def test_market_cap_unit_and_exchange(self):
        count = Mock(text='"1"')
        page = Mock()
        page.json.return_value = [{'symbol':'sz000001','code':'000001','name':'样本',
            'trade':'12.50','changepercent':'1.23','mktcap':123456,
            'ticktime':'11:30:00'}]
        with patch('realtime_quotes.requests.get', side_effect=[count,page]), patch('realtime_quotes.time.sleep'):
            frame = fetch_sina()
        self.assertEqual(frame.iloc[0].ts_code, '000001.SZ')
        self.assertEqual(frame.iloc[0].total_mv / 1e8, 12.3456)
        self.assertEqual(frame.iloc[0].price, 12.5)

    def test_duplicate_universe_is_rejected(self):
        count = Mock(text='"2"')
        page = Mock()
        page.json.return_value = [{'symbol':'sz000001'},{'symbol':'sz000001'}]
        with patch('realtime_quotes.requests.get', side_effect=[count,page]), patch('realtime_quotes.time.sleep'):
            with self.assertRaises(AssertionError):
                fetch_sina()
