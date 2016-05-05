from __future__ import unicode_literals

import pickle

from django.forms import BooleanField, ValidationError
from django.test import SimpleTestCase


class BooleanFieldTest(SimpleTestCase):

    def test_booleanfield_clean_1(self):
        f = BooleanField()
        with self.assertRaisesMessage(ValidationError, "'This field is required.'"):
            f.clean('')
        with self.assertRaisesMessage(ValidationError, "'This field is required.'"):
            f.clean(None)
        self.assertTrue(f.clean(True))
        with self.assertRaisesMessage(ValidationError, "'This field is required.'"):
            f.clean(False)
        self.assertTrue(f.clean(1))
        with self.assertRaisesMessage(ValidationError, "'This field is required.'"):
            f.clean(0)
        self.assertTrue(f.clean('Django rocks'))
        self.assertTrue(f.clean('True'))
        with self.assertRaisesMessage(ValidationError, "'This field is required.'"):
            f.clean('False')

    def test_booleanfield_clean_2(self):
        f = BooleanField(required=False)
        self.assertEqual(False, f.clean(''))
        self.assertEqual(False, f.clean(None))
        self.assertEqual(True, f.clean(True))
        self.assertEqual(False, f.clean(False))
        self.assertEqual(True, f.clean(1))
        self.assertEqual(False, f.clean(0))
        self.assertEqual(True, f.clean('1'))
        self.assertEqual(False, f.clean('0'))
        self.assertEqual(True, f.clean('Django rocks'))
        self.assertEqual(False, f.clean('False'))
        self.assertEqual(False, f.clean('false'))
        self.assertEqual(False, f.clean('FaLsE'))

    def test_boolean_picklable(self):
        self.assertIsInstance(pickle.loads(pickle.dumps(BooleanField())), BooleanField)

    def test_booleanfield_changed(self):
        f = BooleanField()
        self.assertFalse(f.has_changed(None, None))
        self.assertFalse(f.has_changed(None, ''))
        self.assertFalse(f.has_changed('', None))
        self.assertFalse(f.has_changed('', ''))
        self.assertTrue(f.has_changed(False, 'on'))
        self.assertFalse(f.has_changed(True, 'on'))
        self.assertTrue(f.has_changed(True, ''))
        # Initial value may have mutated to a string due to show_hidden_initial (#19537)
        self.assertTrue(f.has_changed('False', 'on'))
