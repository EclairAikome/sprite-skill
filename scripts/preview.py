# -*- coding: utf-8 -*-
"""Render a PDF page to PNG for visual QA (does the page fill top-to-bottom? does any line
wrap badly? is the header clean?). Reading the page numbers is not enough -- look at it.

Usage:
  python scripts/preview.py out/Jane_Doe_DM.pdf            # renders every page to out/_preview_*.png
  python scripts/preview.py out/Jane_Doe_DM.pdf --page 1   # just page index 1 (the resume, when a letter leads)
"""
import argparse
import os


def main():
    import fitz
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--page", type=int, default=None, help="0-based page index; default renders all")
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    d = fitz.open(args.pdf)
    outdir = args.outdir or os.path.dirname(os.path.abspath(args.pdf))
    base = os.path.splitext(os.path.basename(args.pdf))[0]
    pages = [args.page] if args.page is not None else range(d.page_count)
    for i in pages:
        png = os.path.join(outdir, "_preview_%s_p%d.png" % (base, i))
        d[i].get_pixmap(matrix=fitz.Matrix(args.scale, args.scale)).save(png)
        print("rendered", png)
    d.close()


if __name__ == "__main__":
    main()
