PYTHON ?= python

# Paths are repo-relative
STAKEHOLDER_MD   := deliverables/stakeholder_status_update.md
STAKEHOLDER_DOCX := deliverables/stakeholder_status_update.docx
CPRA_MD          := deliverables/calsavers_cpra_request.md
CPRA_DOCX        := deliverables/calsavers_cpra_request.docx

.PHONY: help docs stakeholder-doc cpra-letter clean-derived

help:
	@echo "Targets:"
	@echo "  docs              Regenerate ALL derived docx artifacts."
	@echo "  stakeholder-doc   $(STAKEHOLDER_DOCX) from markdown."
	@echo "  cpra-letter       $(CPRA_DOCX) from markdown."
	@echo "  clean-derived     Remove all derived artifacts."
	@echo ""
	@echo "Markdown is the source of truth; all .docx files are gitignored."
	@echo "Tries pandoc first (better fidelity), falls back to python-docx."
	@echo "Pandoc install: https://pandoc.org/installing.html"

docs: stakeholder-doc cpra-letter

stakeholder-doc: $(STAKEHOLDER_DOCX)
cpra-letter:     $(CPRA_DOCX)

$(STAKEHOLDER_DOCX): $(STAKEHOLDER_MD) scripts/build_doc.py
	$(PYTHON) scripts/build_doc.py "$(STAKEHOLDER_MD)" "$(STAKEHOLDER_DOCX)"

$(CPRA_DOCX): $(CPRA_MD) scripts/build_doc.py
	$(PYTHON) scripts/build_doc.py "$(CPRA_MD)" "$(CPRA_DOCX)"

clean-derived:
	rm -f $(STAKEHOLDER_DOCX) $(CPRA_DOCX)
	@echo "Removed derived artifacts."
