# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# FPaper[dot]Py - Python3 implementation of FPaper (an e-paper file format) (library)
#
# github.com/ferhatgec/fpaper.py
# github.com/ferhatgec/fpaper
#

class FPaperMarkers:
    START_MARKER = b'\x02'
    START_MARKER_2 = b'\x46'
    START_MARKER_3 = b'\x50'
    START_MARKER_4 = b'\x61'
    START_MARKER_5 = b'\x67'
    START_MARKER_6 = b'\x65'

    START_OF_TEXT = b'\x26'
    END_OF_TEXT = b'\x15'

    STYLE_MARKER = b'\x1A'
    LIGHT_SET = b'\x30'
    BOLD_SET = b'\x31'
    DIM_SET = b'\x32'
    ITALIC_SET = b'\x33'

    def __init__(self):
        pass

    def is_start_marker(self, ch) -> bool:
        return True if ch == self.START_MARKER else False

    def is_start_marker_2(self, ch) -> bool:
        return True if ch == self.START_MARKER_2 else False

    def is_start_marker_3(self, ch) -> bool:
        return True if ch == self.START_MARKER_3 else False

    def is_start_marker_4(self, ch) -> bool:
        return True if ch == self.START_MARKER_4 else False

    def is_start_marker_5(self, ch) -> bool:
        return True if ch == self.START_MARKER_5 else False

    def is_start_marker_6(self, ch) -> bool:
        return True if ch == self.START_MARKER_6 else False

    def is_start_of_text(self, ch) -> bool:
        return True if ch == self.START_OF_TEXT else False

    def is_end_of_text(self, ch) -> bool:
        return True if ch == self.END_OF_TEXT else False

    def is_style_marker(self, ch) -> bool:
        return True if ch == self.STYLE_MARKER else False

    def is_light_marker(self, ch) -> bool:
        return True if ch == self.LIGHT_SET else False

    def is_bold_marker(self, ch) -> bool:
        return True if ch == self.BOLD_SET else False

    def is_dim_marker(self, ch) -> bool:
        return True if ch == self.DIM_SET else False

    def is_italic_marker(self, ch) -> bool:
        return True if ch == self.ITALIC_SET else False

class FPaper_Extract:
    def __init__(self, filename: str):
        self.check: FPaperMarkers = FPaperMarkers
        self.filename: str = filename
        self.extracted_text: str = ''

        self.is_start_marker = False
        self.is_start_marker_2 = False
        self.is_start_marker_3 = False
        self.is_start_marker_4 = False
        self.is_start_marker_5 = False
        self.is_start_marker_6 = False

        self.is_start_of_text = False
        self.is_end_of_text = False

        self.is_style_marker = False

    def detect_style(self, ch):
        # Just waiting for 3.10
        # Not platform specific
        if self.check.is_light_marker(self.check, ch):
            self.extracted_text += '\x1b[0m'
        elif self.check.is_bold_marker(self.check, ch):
            self.extracted_text += '\x1b[1m'
        elif self.check.is_dim_marker(self.check, ch):
            self.extracted_text += '\x1b[2m'
        elif self.check.is_italic_marker(self.check, ch):
            self.extracted_text += '\x1b[3m'

    def detect(self, ch):
        if self.is_style_marker:
            self.detect_style(ch)
            self.is_style_marker = False
            return

        if not self.is_start_marker:
            self.is_start_marker = self.check.is_start_marker(self.check, ch)
        elif not self.is_start_marker_2:
            self.is_start_marker_2 = self.check.is_start_marker_2(self.check, ch)
        elif not self.is_start_marker_3:
            self.is_start_marker_3 = self.check.is_start_marker_3(self.check, ch)
        elif not self.is_start_marker_4:
            self.is_start_marker_4 = self.check.is_start_marker_4(self.check, ch)
        elif not self.is_start_marker_5:
            self.is_start_marker_5 = self.check.is_start_marker_5(self.check, ch)
        elif not self.is_start_marker_6:
            self.is_start_marker_6 = self.check.is_start_marker_6(self.check, ch)
        elif not self.is_start_of_text:
            self.is_start_of_text = self.check.is_start_of_text(self.check, ch)
        elif self.is_start_of_text:
            if self.check.is_style_marker(self.check, ch):
                self.is_style_marker = True
                return

            if self.check.is_end_of_text(self.check, ch):
                self.is_end_of_text = True
                return

            self.extracted_text += ch.decode("utf-8")

    def extract(self):
        with open(self.filename, 'rb') as file:
            byte = file.read(1)
            while byte:
                if self.is_end_of_text:
                    break
                self.detect(byte)
                byte = file.read(1)

        print(self.extracted_text)
