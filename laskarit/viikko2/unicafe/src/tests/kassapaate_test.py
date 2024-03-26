
import unittest

from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)
    
    def test_kassassa_rahaa_alussa_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_myytyjen_lounaiden_maara_alussa_oikein(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_toimii_edullisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000 + 2.4)
        self.assertEqual(vaihtoraha, 0)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateisosto_toimii_maukkaalla(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000 + 4)
        self.assertEqual(vaihtoraha, 0)
        self.assertEqual(self.kassapaate.maukkaat, 1)
    
    def test_kateisosto_ei_toimi_edullisella(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.edulliset, 0)
    
    def test_kateisosto_ei_toimi_maukkaalla(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(300)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(vaihtoraha, 300)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_korttiosto_toimii_edullisella(self):
        onnistuiko = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 7.6)
        self.assertEqual(onnistuiko, True)
        self.assertEqual(self.kassapaate.edulliset, 1)
    
    def test_korttiosto_toimii_maukkaalla(self):
        onnistuiko = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6)
        self.assertEqual(onnistuiko, True)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_korttiosto_ei_toimi_edullisella(self):
        self.maksukortti.ota_rahaa(800)
        onnistuiko = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2)
        self.assertEqual(onnistuiko, False)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_korttiosto_ei_toimi_maukkaalla(self):
        self.maksukortti.ota_rahaa(800)
        onnistuiko = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2)
        self.assertEqual(onnistuiko, False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
    
    def test_kassa_ei_muutu_korttiostossa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_kortille_lataaminen_toimii(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 15.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000 + 5)

    def test_kortille_lataaminen_negatiivisella_summalla_ei_muuta_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_nollan_lataaminen_ei_muuta_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 0)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
