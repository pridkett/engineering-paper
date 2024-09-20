Engineering Paper Generator
===========================

Patrick Wagstrom &lt;160672+pridkett@users.noreply.github.com&gt;

September 2024

Overview
--------

This is a simple program born of a need. That need was to generate a decent PDF of engineering paper that I could use as a background for programs like Notability and GoodNotes. For some reason, neither of those programs had good templates for engineering paper.

While there are other templates out there, there was another complicating factor that the default text margins for these programs are quite small. While that's easy to deal with on the top and the bottom of the page, I'd rather not deal with it on the left and right sides of the page where I need to manage it on every line of text.

Example Usage
-------------

Create a sheet of 8.5x11 inch engineering paper with somewhat standard margins.

```bash
python paper.py custom_engineering_paper.pdf
```

Create a sheet of A4 engineering paper with somewhat standard margins.

```bash
python paper.py --paper-size A4 custom_engineering_paper.pdf
```

License
-------

Copyright (c) 2024 Patrick Wagstrom

Licened under the terms of the MIT License. See the LICENSE file for details.