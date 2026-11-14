import unittest
from src.aml import monitor, validate_cases

class TestAML(unittest.TestCase):
    def test_high_deposit_alert(self):
        alerts=monitor([{'customer_id':'A','typical_deposit_cad':'500'}],[{'customer_id':'A','transaction_id':'1','timestamp':'2026-11-01T10:00:00','type':'deposit','amount_cad':'4000'}])
        self.assertEqual(len(alerts),1)
    def test_rapid_withdrawal(self):
        tx=[{'customer_id':'A','transaction_id':'1','timestamp':'2026-11-01T10:00:00','type':'deposit','amount_cad':'500'}, {'customer_id':'A','transaction_id':'2','timestamp':'2026-11-01T11:00:00','type':'crypto_withdrawal','amount_cad':'400'}]
        self.assertEqual(len(monitor([{'customer_id':'A','typical_deposit_cad':'500'}],tx)),1)
    def test_mismatch(self):
        case={'case_id':'1','customer_id':'A','transaction_id':'T','transaction_date':'2026-11-01','reported_amount_cad':'100','source_amount_cad':'200'}
        self.assertEqual(validate_cases([case])[0]['status'],'Review required')
    def test_valid(self):
        case={'case_id':'1','customer_id':'A','transaction_id':'T','transaction_date':'2026-11-01','reported_amount_cad':'100','source_amount_cad':'100'}
        self.assertEqual(validate_cases([case])[0]['status'],'Checks passed')

if __name__=='__main__': unittest.main()
