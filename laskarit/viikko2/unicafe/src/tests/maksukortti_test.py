import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 20)

    def test_ottaminen_vahentaa_saldoa_oikein(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5)

    def test_ottaminen_ei_vie_saldoa_negatiiviseksi(self):
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_ottaminen_palauttaa_true_jos_rahat_riittivat(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_ottaminen_palauttaa_false_jos_rahat_eivat_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(2000), False)