PYTHON ?= python

# Paths are repo-relative
STAKEHOLDER_MD   := deliverables/stakeholder_status_update.md
STAKEHOLDER_DOCX := deliverables/stakeholder_status_update.docx

.PHONY: help stakeholder-doc clean-derived

help:
	@echo "Targets:"
	@echo "  stakeholder-doc   Regenerate $(STAKEHOLDER_DOCX) from $(STAKEHOLDER_MD)."
	@echo "                    Markdown is the source of truth; .docx is gitignored."
	@echo "  clean-derived     Remove derived artifacts (the .docx)."
	@echo ""
	@echo "Tries pandoc first (better fidelity), falls back to python-docx."
	@echo "Pandoc install: https://pandoc.org/installing.html"

stakeholder-doc: $(STAKEHOLDER_DOCX)

$(STAKEHOLDER_DOCX): $(STAKEHOLDER_MD) scripts/build_stakeholder_doc.py
	$(PYTHON) scripts/build_stakeholder_doc.py

clean-derived:
	rm -f $(STAKEHOLDER_DOCX)
	@echo "Removed derived artifacts."
