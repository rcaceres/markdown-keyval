"""
KeyValue Extension for Python-Markdown
=============================================

A simple example:

Apple: Pomaceous fruit of plants of the genus Malus in.
Orange: The fruit of an evergreen tree of the genus Citrus.

@todo get this to print out in a table
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.blockprocessors import BlockProcessor, ListIndentProcessor
from markdown.util import etree
import re


class KeyValProcessor(BlockProcessor):
    """ Process Key Value Pairs. """

    # Regex for key value
    RE = re.compile(r'^(?P<key>[^\s]+):\s+(?P<value>.+)(\n|$)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()] # All lines before header
            after = block[m.end():]    # All lines after header
            #if before:
            #    # As the header was not the first line of the block and the
            #    # lines before the header must be parsed first,
            #    # recursively parse this lines as a block.
            #    self.parser.parseBlocks(parent, [before])
            
            # Create header using named groups from RE
            h = etree.SubElement(parent, 'div')
            #template = "<dl><dt>%s</dt><dd>%s</dd></dl>"
            template = "<b>%s</b>: %s"
            #template = "<tr><td>%s</td><td>%s</td></tr>"
            h.text = template % (m.group('key').strip(), m.group('value').strip())
            if after:
                # Insert remaining lines as first block for future parsing.
                blocks.insert(0, after)
        else:
            # This should never happen, but just in case...
            logger.warn("We've got a problem header: %r" % block)


class KeyValExtension(Extension):
    """ Add keyvalues to Markdown. """

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('keyval', KeyValProcessor(md.parser), '>ulist')


def makeExtension(configs={}):
    return KeyValExtension(configs=configs)
