#
# Copyright (C) 2007-2011 Edgewall Software, 2013-2022 the Babel team
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution. The terms
# are also available at http://babel.edgewall.org/wiki/License.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://babel.edgewall.org/log/.

import unittest
from datetime import datetime
from io import BytesIO

from babel import __version__ as VERSION
from babel.core import Locale, UnknownLocaleError
from babel.dates import format_datetime
from babel.messages import checkers
from babel.messages.plurals import PLURALS
from babel.messages.pofile import read_po
from babel.util import LOCALTZ


class CheckersTestCase(unittest.TestCase):
    # the last msgstr[idx] is always missing except for singular plural forms

    def test_1_num_plurals_checkers(self):
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 1]:
            try:
                locale = Locale.parse(_locale)
            except UnknownLocaleError:
                # Just an alias? Not what we're testing here, let's continue
                continue
            date = format_datetime(datetime.now(LOCALTZ), 'yyyy-MM-dd HH:mmZ', tzinfo=LOCALTZ, locale=_locale)
            plural = PLURALS[_locale][0]
            po_file = (f"""\
# {locale.english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\\n"
"PO-Revision-Date: {date}\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: {_locale} <LL@li.org>\n"
"Plural-Forms: nplurals={plural}; plural={plural};\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: Babel {VERSION}\\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""

""").encode('utf-8')

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)

    def test_2_num_plurals_checkers(self):
        # in this testcase we add an extra msgstr[idx], we should be
        # disregarding it
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 2]:
            if _locale in ['nn', 'no']:
                _locale = 'nn_NO'
                num_plurals = PLURALS[_locale.split('_')[0]][0]
                plural_expr = PLURALS[_locale.split('_')[0]][1]
            else:
                num_plurals = PLURALS[_locale][0]
                plural_expr = PLURALS[_locale][1]
            try:
                locale = Locale(_locale)
                date = format_datetime(datetime.now(LOCALTZ),
                                       'yyyy-MM-dd HH:mmZ',
                                       tzinfo=LOCALTZ, locale=_locale)
            except UnknownLocaleError:
                # Just an alias? Not what we're testing here, let's continue
                continue
            po_file = f"""\
# {locale.english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\\n"
"PO-Revision-Date: {date}\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: {_locale} <LL@li.org>\\n"
"Plural-Forms: nplurals={num_plurals}; plural={plural_expr};\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: Babel {VERSION}\\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""
msgstr[2] ""

""".encode('utf-8')
            # we should be adding the missing msgstr[0]

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)

    def test_3_num_plurals_checkers(self):
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 3]:
            plural = format_datetime(datetime.now(LOCALTZ), 'yyyy-MM-dd HH:mmZ', tzinfo=LOCALTZ, locale=_locale)
            english_name = Locale.parse(_locale).english_name
            po_file = fr"""\
# {english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\n"
"PO-Revision-Date: {plural}\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: {_locale} <LL@li.org>\n"
"Plural-Forms: nplurals={PLURALS[_locale][0]}; plural={PLURALS[_locale][0]};\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel {VERSION}\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""

""".encode('utf-8')

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)

    def test_4_num_plurals_checkers(self):
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 4]:
            date = format_datetime(datetime.now(LOCALTZ), 'yyyy-MM-dd HH:mmZ', tzinfo=LOCALTZ, locale=_locale)
            english_name = Locale.parse(_locale).english_name
            plural = PLURALS[_locale][0]
            po_file = fr"""\
# {english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\n"
"PO-Revision-Date: {date}\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: {_locale} <LL@li.org>\n"
"Plural-Forms: nplurals={plural}; plural={plural};\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel {VERSION}\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""
msgstr[2] ""

""".encode('utf-8')

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)

    def test_5_num_plurals_checkers(self):
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 5]:
            date = format_datetime(datetime.now(LOCALTZ), 'yyyy-MM-dd HH:mmZ', tzinfo=LOCALTZ, locale=_locale)
            english_name = Locale.parse(_locale).english_name
            plural = PLURALS[_locale][0]
            po_file = fr"""\
# {english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\n"
"PO-Revision-Date: {date}\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: {_locale} <LL@li.org>\n"
"Plural-Forms: nplurals={plural}; plural={plural};\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel {VERSION}\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""
msgstr[2] ""
msgstr[3] ""

""".encode('utf-8')

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)

    def test_6_num_plurals_checkers(self):
        for _locale in [p for p in PLURALS if PLURALS[p][0] == 6]:
            english_name = Locale.parse(_locale).english_name
            date = format_datetime(datetime.now(LOCALTZ), 'yyyy-MM-dd HH:mmZ', tzinfo=LOCALTZ, locale=_locale)
            plural = PLURALS[_locale][0]
            po_file = fr"""\
# {english_name} translations for TestProject.
# Copyright (C) 2007 FooBar, Inc.
# This file is distributed under the same license as the TestProject
# project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2007.
#
msgid ""
msgstr ""
"Project-Id-Version: TestProject 0.1\n"
"Report-Msgid-Bugs-To: bugs.address@email.tld\n"
"POT-Creation-Date: 2007-04-01 15:30+0200\n"
"PO-Revision-Date: {date}\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: {_locale} <LL@li.org>\n"
"Plural-Forms: nplurals={plural}; plural={plural};\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel {VERSION}\n"

#. This will be a translator comment,
#. that will include several lines
#: project/file1.py:8
msgid "bar"
msgstr ""

#: project/file2.py:9
msgid "foobar"
msgid_plural "foobars"
msgstr[0] ""
msgstr[1] ""
msgstr[2] ""
msgstr[3] ""
msgstr[4] ""

""".encode('utf-8')

            # This test will fail for revisions <= 406 because so far
            # catalog.num_plurals was neglected
            catalog = read_po(BytesIO(po_file), _locale)
            message = catalog['foobar']
            checkers.num_plurals(catalog, message)
