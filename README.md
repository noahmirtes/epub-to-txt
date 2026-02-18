# epub-to-txt
A simple script to extract text from .epub files in a structured form and save to a .txt file

I have accumulated a large library of .epubs over the years. An issue I've encountered as of late, especially in an AI assisted world, is that all the text and knowledge is locked away in the files. Sure, many LLMs can parse and read .epub files, but I often prefer to work with .txt files since they're so ubiquitous and can be read and editied very easily. This is for a few reasons:

- If I want to use a book to inform decisions about a project that I'm planning with an LLM, an .epub will work, but I simply prefer .txt.
- Most epubs contain chapters with irrelevant information to an LLM that can confuse and bloat the context window. By parsing the .epub and not extracting potentially useless chapters to the output .txt, you get a more focused and useful document to pass to LLMs.
- LLMs make stuff up! If it's citing something from the text I gave it, I have to open the .epub in a book viewer of some kind, which isn't always easy depending on the machine I'm on. Opening up a .txt file is simple and and straight forward on every machine.

To solve this "problem", I made this small script that parses the epub, performs some general checks to skip unimportant chapters, and writes the text to a .txt file with the original chapter/paragraph formatting.

To use this script:
- Specify an input path for a folder that the .epubs are in (the script will search this folder recursively for all .epub files).
- Specify an output path for the folder that the .txt files should be saved to.
- Run!

A couple notes on the chapter filtering:
- My default setting is that a chapter must be at least 200 characters in order to count as a valid chapter and be included in the output. This is customizable to be more or less strict.
- The output .txt file can optionally be saved with a dashed line separating the chapters for improved readability.
- Not every epub is formatted the same, so there is a fallback to grab all the text from a chapter. This does not retain paragraph formatting, so the outputted text will have all text from the chapter chunked together in large, unbroken blocks where this is the case.
