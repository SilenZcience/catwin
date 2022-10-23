import sys
sys.path.append("../cat_win")

from unittest import TestCase
from unittest.mock import patch

from cat_win.util.Converter import Converter

expected_output = ""

converter = Converter()

class TestConverter(TestCase):
    def test_converter_dec(self):
        expected_output = "12345 {Hexadecimal: 0x3039; Binary: 0b11000000111001}"
        self.assertEqual(converter._fromDEC(12345, True), expected_output)
        
        expected_output = "12345 {Hexadecimal: 3039; Binary: 11000000111001}"
        self.assertEqual(converter._fromDEC(12345, False), expected_output)
        
    def test_converter_hex(self):
        expected_output = "0x3039 {Decimal: 12345; Binary: 0b11000000111001}"
        self.assertEqual(converter._fromHEX("0x3039", True), expected_output)
        
        expected_output = "0x3039 {Decimal: 12345; Binary: 11000000111001}"
        self.assertEqual(converter._fromHEX("0x3039", False), expected_output)
        
        expected_output = "3039 {Decimal: 12345; Binary: 0b11000000111001}"
        self.assertEqual(converter._fromHEX("3039", True), expected_output)
        
        expected_output = "3039 {Decimal: 12345; Binary: 11000000111001}"
        self.assertEqual(converter._fromHEX("3039", False), expected_output)
            
    def test_converter_bin(self):
        expected_output = "0b11000000111001 {Decimal: 12345; Hexadecimal: 0x3039}"
        self.assertEqual(converter._fromBIN("0b11000000111001", True), expected_output)
        
        expected_output = "0b11000000111001 {Decimal: 12345; Hexadecimal: 3039}"
        self.assertEqual(converter._fromBIN("0b11000000111001", False), expected_output)
        
        expected_output = "11000000111001 {Decimal: 12345; Hexadecimal: 0x3039}"
        self.assertEqual(converter._fromBIN("11000000111001", True), expected_output)
        
        expected_output = "11000000111001 {Decimal: 12345; Hexadecimal: 3039}"
        self.assertEqual(converter._fromBIN("11000000111001", False), expected_output)

#python -m unittest discover -s tests -p test*.py