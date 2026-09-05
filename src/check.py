# -*- coding: utf-8 -*-
"""Check that ../index.html is what build.py currently produces.

The shipped page is generated, so the thing that goes wrong is that somebody
edits it directly, or edits a deck and forgets to build. Either way the next
build silently reverts their work. Run this before committing.
"""
import io, os, sys, contextlib, pathlib

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

import build

shipped = pathlib.Path('../index.html')
was = shipped.read_text(encoding='utf-8')
with contextlib.redirect_stdout(io.StringIO()):
    build.main()
now = shipped.read_text(encoding='utf-8')

if was != now:
    shipped.write_text(was, encoding='utf-8')  # leave the tree as we found it
    sys.exit('../index.html is not what build.py produces. Either it was edited '
             'by hand, or a deck changed and was never built. Run: python3 build.py')

for marker in ('/*@INSTRUMENTS@*/', '/*@WORDS@*/', '/*@ENGINES@*/'):
    if pathlib.Path('template.html').read_text(encoding='utf-8').count(marker) != 1:
        sys.exit('template.html has lost its %s marker' % marker)

print('ok — index.html matches the build, all three markers present')
