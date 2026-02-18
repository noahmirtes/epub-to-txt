# main.py
import os
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

path = "/Users/noah/REPOS/epub_to_text/input/The Penguin History of the Twentieth Century_The History of.epub"
output_folder = "/Users/noah/REPOS/epub_to_text/output"
book = epub.read_epub(path)

# ----------------------------------------------------- #

def extract_epub_text(path : str, min_chapter_len : int = 200, chapter_separator=False):
    """
    Extract the text from an epub and save to .txt in a structured format

    min_chapter_len : the minimim number of characters a chapter must be to be extracted
    chapter_separated : include a dashed line to s
    """
    book = epub.read_epub(path)

    # skip if these words detected in. Must be lowercase
    skip_checks = [
        "table of contents",
        "foreword",
        "afterword",
        "index",
        "acknowledgements",
        "about the author",
        "also available",
        "published",
        "bookseller",
    ]

    text_blocks = []
    for idref, linear in book.spine:
        # skip non-linear items
        if linear == "no":
            continue

        # get the actual document by ID
        item = book.get_item_with_id(idref)
        if item.get_type() != ITEM_DOCUMENT:
            continue
        soup = BeautifulSoup(item.get_content(), "html.parser")

        chapter_pars = soup.find_all('p')

        paragraphs = [p.get_text() for p in chapter_pars]
        paragraphs = [p for p in paragraphs if p]

        chapter_text = None
        if len(paragraphs) > 0:
            chapter_text = "\n\n".join(paragraphs)
        if not chapter_text:
            chapter_text = soup.get_text()
        
        # skip short chapters
        chapter_len = len(chapter_text)
        if chapter_len < min_chapter_len:
            continue

        # trim chapter text for skip check
        ref_text = chapter_text[:300]
        if any(skip in ref_text for skip in skip_checks):
            continue

        # store chapter text
        text_blocks.append(chapter_text.strip())

    
    # join all text blocks and return
    if chapter_separator:
        separator = f"\n\n{"-" * 50}\n\n"
    else:
        separator = "\n\n"
    return separator.join(text_blocks)

def get_files_with_extensions(folder_path: str, target_exts: list[str]):
    """
    Recursively collect all files under folder_path
    that match any extension in target_exts.
    
    target_exts example: [".epub", ".txt", ".pdf"]
    """

    # normalize extensions
    normalized_exts = []
    for ext in target_exts:
        if not ext.startswith("."):
            ext = "." + ext
        normalized_exts.append(ext.lower())

    matches = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if any(filename.lower().endswith(ext) for ext in normalized_exts):
                full_path = os.path.join(root, filename)
                matches.append(full_path)

    return matches

def write_to_txt(path : str, text : str):
    """Write text to a .txt file at the specified path"""
    try:
        with open(path, 'w', encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Could not write to .txt : {e}")

# ----------------------------------------------------- #

def main(input_folder, output_folder):
    """
    The main entry point that takes in a path that contains .epub files and extracts their text in a structured format to .txt
    """

    book_paths = get_files_with_extensions(input_folder, ['.epub'])

    for path in book_paths:
        try:
            # extract the text from the book
            book_text = extract_epub_text(
                path=path,
                min_chapter_len=200,
                chapter_separator=True
            )
            
            # build output path
            path_no_ext = os.path.splitext(path)[-2]
            basename = os.path.basename(path_no_ext)
            output_path = os.path.join(output_folder, f"{basename}.txt")
            
            # write book text to file
            write_to_txt(output_path, book_text)
            print(f"Extracted and saved {basename}")

        except Exception as e:
            print(f"Issue reading epub at : {path} : {e}")

# ----------------------------------------------------- #


if __name__ == "__main__":

    input_folder = "/Volumes/FILES/Noah's Library/Nonfiction"
    output_folder = "/Users/noah/REPOS/local_researcher/epub_text"
    main(input_folder, output_folder)

