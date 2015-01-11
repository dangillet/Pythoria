#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MessageBox(list):
    def __init__(self, width=18, height=5, *msgs):
        super(MessageBox, self).__init__(msgs)
        self.width, self.height = width, height

    def add(self, msg):
        super(MessageBox, self).__init__(self._text_wrap('\n'.join(self+[msg])))

    def _text_wrap(self, *msgs):
        joined = '\n'.join(msgs)
        potential_split_index = []
        for i, char in enumerate(joined):
            if char in ('\n', ' '):
                potential_split_index.append(i)

        lines = []
        last = 0

        for i, pos in enumerate(potential_split_index):
            if pos == self.width:
                lines.append(joined[last:pos])
                last = pos
            elif pos > self.width:
                lines.append(joined[last:potential_split_index[i-1]])
                last = potential_split_index[i-1]
        return lines