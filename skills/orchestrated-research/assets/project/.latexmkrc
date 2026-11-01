# Keep the PDF here. Auxiliary files go to .build/latex.
$aux_dir = '.build/latex';
$out_dir = '.';
$emulate_aux = 1;
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error %O %S';
