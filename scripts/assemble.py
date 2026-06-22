# -*- coding: utf-8 -*-
"""sprite-skill assembler: turn a tailored resume (+ optional cover letter) into the
final deliverable PDF and verify the hard rules.

Pipeline:
  1. Render resume .docx (resume_lib.build_resume) for the chosen variant.
  2. Render cover-letter .docx (resume_lib.render_cover_letter) unless --no-letter.
  3. Export each .docx -> PDF (Word COM on Windows; LibreOffice `soffice` fallback),
     all in ONE Word session.
  4. Verify the RESUME is exactly one page (and the letter is one page). Warn loudly otherwise.
  5. Merge: cover letter = page 1, resume = page 2 (rule: every deliverable PDF leads with
     a tailored cover letter). With --no-letter / --resume-only, emit the resume alone.
  6. If the final PDF exceeds --max-mb (default 2), recompress; report the final size.
  7. Clean up intermediate .docx/.pdf.

Usage:
  python scripts/assemble.py --variant DM --letter cover_letter_DM.md
  python scripts/assemble.py --variant PM --no-letter --out out/Resume_PM.pdf
  python scripts/assemble.py --variant DM --drop-soft   # low-touch role: no volunteer/additional

One-page is a HARD rule. If a page overflows, do NOT just shrink the font to nothing --
adjust content and `line_spacing` in candidate.py (see references/guardrails.md) and re-run.
The line-spacing -> page-count relationship is NOT linear; iterate and re-check.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resume_lib as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def page_count(pdf_path):
    import fitz
    d = fitz.open(pdf_path); n = d.page_count; d.close(); return n


def export_batch(pairs):
    """Export many (.docx -> .pdf) in ONE session. Returns {docx_path: (pages, words|None)}.

    Prefers Word COM (best .docx fidelity) via a dedicated instance (DispatchEx, so we never
    quit the user's own Word). Falls back to LibreOffice `soffice` if Word/pywin32 is missing.
    """
    results = {}
    try:
        import win32com.client  # type: ignore
        word = win32com.client.DispatchEx("Word.Application")  # dedicated instance
        word.Visible = False
        try:
            word.DisplayAlerts = 0
        except Exception:
            pass
        try:
            for docx_path, pdf_path in pairs:
                doc = word.Documents.Open(os.path.abspath(docx_path))
                doc.Repaginate()
                pages = int(doc.ComputeStatistics(2))   # wdStatisticPages
                words = int(doc.ComputeStatistics(0))   # wdStatisticWords
                doc.ExportAsFixedFormat(os.path.abspath(pdf_path), 17)  # 17 = wdExportFormatPDF
                doc.Close(False)
                results[docx_path] = (pages, words)
        finally:
            try:
                word.Quit()
            except Exception:
                pass
        return results
    except Exception as e:
        import shutil
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            raise RuntimeError(
                "Could not export PDF: Word COM unavailable (%s) and no LibreOffice found.\n"
                "Install pywin32 + Microsoft Word (Windows), or LibreOffice (cross-platform)." % e)
        import subprocess
        for docx_path, pdf_path in pairs:
            out_dir = os.path.dirname(os.path.abspath(pdf_path))
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", out_dir,
                            os.path.abspath(docx_path)], check=True, capture_output=True)
            produced = os.path.join(out_dir, os.path.splitext(os.path.basename(docx_path))[0] + ".pdf")
            if os.path.abspath(produced) != os.path.abspath(pdf_path) and os.path.exists(produced):
                os.replace(produced, pdf_path)
            results[docx_path] = (page_count(pdf_path), None)
        return results


def merge(pdfs, out_path, max_mb=2.0):
    import fitz
    m = fitz.open()
    for p in pdfs:
        m.insert_pdf(fitz.open(p))
    m.save(out_path, deflate=True, garbage=4)
    n = m.page_count
    m.close()
    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    if size_mb > max_mb:
        # Text resumes rarely exceed 2 MB; if they do it is almost always an embedded raster.
        m2 = fitz.open(out_path)
        m2.save(out_path, deflate=True, deflate_images=True, garbage=4, clean=True)
        m2.close()
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
    return n, size_mb


def main():
    ap = argparse.ArgumentParser(description="Assemble the final sprite-skill resume PDF.")
    ap.add_argument("--variant", required=True, help="key into candidate.VARIANTS (e.g. DM, PM)")
    ap.add_argument("--candidate", default=os.path.join(ROOT, "candidate.py"),
                    help="path to candidate.py (default: repo-root/candidate.py)")
    ap.add_argument("--letter", default=None, help="path to the cover-letter .md (page 1)")
    ap.add_argument("--no-letter", action="store_true", help="resume only, no cover letter page")
    ap.add_argument("--drop-soft", action="store_true",
                    help="drop Volunteer + Additional (low-touch / non-people-facing roles)")
    ap.add_argument("--out", default=None, help="final PDF path")
    ap.add_argument("--max-mb", type=float, default=2.0, help="compress if final PDF exceeds this")
    args = ap.parse_args()

    if not os.path.exists(args.candidate):
        sys.exit("candidate.py not found at %s -- copy assets/candidate.example.py to %s and fill it in."
                 % (args.candidate, os.path.join(ROOT, "candidate.py")))
    cand = R.load_candidate(args.candidate)

    out_dir = os.path.join(ROOT, "out"); os.makedirs(out_dir, exist_ok=True)
    final = args.out or os.path.join(out_dir, "%s_%s.pdf" % (cand.IDENTITY["name"].replace(" ", "_"), args.variant))

    tmp = []
    # 1) render docx (resume + optional letter)
    resume_docx = os.path.join(out_dir, "_resume_%s.docx" % args.variant); tmp.append(resume_docx)
    R.build_resume(cand, args.variant, resume_docx, drop_soft=args.drop_soft)
    resume_pdf = os.path.join(out_dir, "_resume_%s.pdf" % args.variant); tmp.append(resume_pdf)

    jobs = [(resume_docx, resume_pdf)]
    use_letter = bool(args.letter) and not args.no_letter
    letter_pdf = None
    if use_letter:
        letter_docx = os.path.join(out_dir, "_letter_%s.docx" % args.variant); tmp.append(letter_docx)
        R.render_cover_letter(cand, args.letter, letter_docx)
        letter_pdf = os.path.join(out_dir, "_letter_%s.pdf" % args.variant); tmp.append(letter_pdf)
        jobs.append((letter_docx, letter_pdf))

    # 2) export everything in one Word session
    res = export_batch(jobs)

    rp, rw = res[resume_docx]
    print("[resume] pages=%s words=%s  %s" % (rp, rw, "OK" if rp == 1 else "OVERFLOW"))
    if rp != 1:
        print("  !! Resume is %s pages. Trim content or adjust VARIANTS['%s']['line_spacing'] in candidate.py, then re-run."
              % (rp, args.variant))

    pages_to_merge = []
    if use_letter:
        lp, lw = res[jobs[1][0]]
        print("[letter] pages=%s words=%s  %s" % (lp, lw, "OK" if lp == 1 else "OVERFLOW"))
        if lp != 1:
            print("  !! Cover letter is %s pages. Tighten the letter .md, then re-run." % lp)
        pages_to_merge.append(letter_pdf)
    pages_to_merge.append(resume_pdf)

    n, size_mb = merge(pages_to_merge, final, max_mb=args.max_mb)
    size_note = "OK (<= %.1fMB)" % args.max_mb if size_mb <= args.max_mb else "STILL > %.1fMB" % args.max_mb
    print("[final ] %s  pages=%d  size=%.2fMB  %s" % (final, n, size_mb, size_note))

    for f in tmp:
        try:
            os.remove(f)
        except OSError:
            pass


if __name__ == "__main__":
    main()
