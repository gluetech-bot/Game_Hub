MAIN = report

$(MAIN).pdf: $(MAIN).tex
	pdflatex $(MAIN).tex
	bibtex $(MAIN)
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex

all: $(MAIN).pdf

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.run.xml
