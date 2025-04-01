Toolkit for playing the game Cypher. The goal is to mitigate the tedious part of the game, and functions are intentionally NOT streamlined, 
so that you can still have some fun solving the puzzles.

To see an example of solving polyalphabetic substition with vignere square, see `solve_poly2.py`.
Get the word segmentation tool `wordsegment` here: https://pypi.org/project/wordsegment/

To see an example of decoding using a Enigma prototype with basic helper functions, see `solve_enigma1.py`.

To see an example of decoding using a Enigma prototype with the Scramblers class, see `solve_enigma2.py`.

To run enigma encoding/decoding, use the run_enigma.py script. It takes the following argument:
`input`: Input text or file name containing the text.
`--config` or `-c`: Enigma machine configuration file.
`--outfile` or `-o`: Output file name. If not specified, the decoded text is printed to the terminal.

The configuration file must contain at least one scrambler and one reflector. Swapper and initial key is optional.
The reflector can be specified as either a string or a list of letter pairs.
For examples of configuration file, see `enigma_default.json` and `enigma_simple.json`.