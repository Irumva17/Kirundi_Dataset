#!/usr/bin/env python3
"""
Script d'extraction OCR pour les PDFs de lois (screenshots/images).
Produit pour chaque PDF:
  - Un fichier .txt avec le texte extrait
  - Un fichier _text.pdf avec le texte en format PDF
"""

import os
import sys
import time
import functools
from pathlib import Path

from pdf2image import convert_from_path
import tesserocr
from PIL import Image
from fpdf import FPDF

# Force unbuffered print
print = functools.partial(print, flush=True)

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
TESSDATA_DIR = SCRIPT_DIR.parent / "tessdata"
OCR_LANG = "fra"  # French - les lois sont en français
DPI = 200  # Resolution for image conversion (200 is good balance speed/quality)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extrait le texte d'un PDF image page par page.
    Traite une page à la fois pour économiser la mémoire.
    """
    pdf_path = Path(pdf_path)
    print(f"\n{'='*60}")
    print(f"Extraction du texte: {pdf_path.name}")
    print(f"{'='*60}")

    # Get total page count first
    from pdf2image.pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(str(pdf_path))
    total_pages = info["Pages"]
    print(f"Nombre de pages: {total_pages}")

    all_text = []
    start_time = time.time()

    with tesserocr.PyTessBaseAPI(path=str(TESSDATA_DIR), lang=OCR_LANG) as api:
        for page_num in range(1, total_pages + 1):
            page_start = time.time()

            # Convert single page to image
            images = convert_from_path(
                str(pdf_path),
                dpi=DPI,
                first_page=page_num,
                last_page=page_num,
            )

            if not images:
                print(f"  Page {page_num}/{total_pages}: ERREUR - pas d'image")
                continue

            img = images[0]

            # OCR the page
            api.SetImage(img)
            page_text = api.GetUTF8Text().strip()

            page_time = time.time() - page_start
            elapsed = time.time() - start_time
            avg_per_page = elapsed / page_num
            remaining = avg_per_page * (total_pages - page_num)

            print(
                f"  Page {page_num:3d}/{total_pages} "
                f"({page_time:.1f}s) "
                f"[{len(page_text)} chars] "
                f"- Restant: ~{remaining/60:.1f} min"
            )

            all_text.append(f"--- Page {page_num} ---\n{page_text}")

            # Free memory
            del images, img

    full_text = "\n\n".join(all_text)
    total_time = time.time() - start_time
    print(f"\nTerminé en {total_time/60:.1f} minutes")
    print(f"Total: {len(full_text)} caractères extraits")

    return full_text


def save_text_file(text: str, output_path: Path):
    """Sauvegarde le texte extrait dans un fichier .txt"""
    output_path = Path(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    size_kb = output_path.stat().st_size / 1024
    print(f"Fichier TXT sauvegardé: {output_path.name} ({size_kb:.1f} KB)")


def save_text_pdf(text: str, output_path: Path):
    """Crée un PDF contenant le texte extrait."""
    output_path = Path(output_path)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(10, 10, 10)

    # Use a built-in font that supports basic Latin characters
    pdf.add_page()
    pdf.set_font("Helvetica", size=9)

    # Split text into lines and add to PDF
    for line in text.split("\n"):
        # Handle page separators
        if line.startswith("--- Page "):
            pdf.set_font("Helvetica", "B", size=11)
            pdf.cell(0, 8, line, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=9)
        else:
            # Encode to latin-1 for built-in font compatibility
            safe_line = line.encode("latin-1", errors="replace").decode("latin-1")
            # Truncate extremely long words that would overflow
            words = safe_line.split()
            safe_words = [w[:80] if len(w) > 80 else w for w in words]
            safe_line = " ".join(safe_words)
            try:
                pdf.multi_cell(0, 4, safe_line)
            except Exception:
                # If a line still fails, skip it
                pass

    pdf.output(str(output_path))
    size_kb = output_path.stat().st_size / 1024
    print(f"Fichier PDF texte sauvegardé: {output_path.name} ({size_kb:.1f} KB)")


def process_pdf(pdf_path: Path, txt_only: bool = False):
    """Traite un PDF: extraction texte -> .txt (+ .pdf si txt_only=False)"""
    pdf_path = Path(pdf_path)
    stem = pdf_path.stem

    # Output paths
    txt_path = pdf_path.parent / f"{stem}.txt"
    text_pdf_path = pdf_path.parent / f"{stem}_text.pdf"

    # Extract text via OCR
    text = extract_text_from_pdf(pdf_path)

    if not text.strip():
        print(f"ATTENTION: Aucun texte extrait de {pdf_path.name}!")
        return

    # Save as TXT
    save_text_file(text, txt_path)

    # Save as text PDF (unless txt_only mode)
    if not txt_only:
        save_text_pdf(text, text_pdf_path)

    print(f"\nFichiers créés pour {pdf_path.name}:")
    print(f"  - {txt_path.name}")
    if not txt_only:
        print(f"  - {text_pdf_path.name}")


def main():
    """Point d'entrée principal."""
    # Find all PDF files in the lois directory (excluding _text.pdf outputs)
    pdf_files = sorted([
        f for f in SCRIPT_DIR.glob("*.pdf")
        if not f.stem.endswith("_text") and not f.stem.endswith("_ocr")
    ])

    if not pdf_files:
        print("Aucun fichier PDF trouvé dans le dossier lois/")
        sys.exit(1)

    print(f"Fichiers PDF à traiter: {len(pdf_files)}")
    for f in pdf_files:
        print(f"  - {f.name} ({f.stat().st_size / 1024 / 1024:.1f} MB)")

    # Parse arguments: [filter] [--txt-only]
    txt_only = "--txt-only" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--txt-only"]

    if args:
        target = args[0]
        pdf_files = [f for f in pdf_files if target in f.name]
        if not pdf_files:
            print(f"Aucun PDF correspondant à '{target}'")
            sys.exit(1)

    if txt_only:
        print("Mode: TXT seulement (pas de PDF texte)")

    total_start = time.time()
    for pdf_path in pdf_files:
        process_pdf(pdf_path, txt_only=txt_only)

    total_time = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"Tous les traitements terminés en {total_time/60:.1f} minutes")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
