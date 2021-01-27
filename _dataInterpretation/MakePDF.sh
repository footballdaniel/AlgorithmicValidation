echo Requires PANDOC to be installed
echo Requires SVGCONVERT to be installed
echo Requires TEX e.g. MIKTEX to be installed

echo === START COMPILING DOCUMENT ===

pandoc -s summary.md -o summary.pdf

echo === FINISH COMPILING DOCUMENT ===

# Opens shell and prevents closing on error
$SHELL
