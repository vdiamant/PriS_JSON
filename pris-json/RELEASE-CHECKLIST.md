# Release checklist (for the authors – delete this file before publishing)

1. **Fill the placeholders** in `README.md` and `CITATION.cff`: `[MANUSCRIPT TITLE]`, `[JOURNAL]`,
   `[YEAR]`, author names and ORCIDs.
2. **Confirm the provenance** of Listing 3: the manuscript currently attributes the Career Office JSON
   instantiation to [28] in Section 7.3 and to [29] a page later. Use the same source in the manuscript
   and in `README.md` → *Provenance*.
3. **PriS-Tool.** Choose one statement and put it in `README.md` → *Not included* and in the
   manuscript's Code Availability statement:
   - *Available:* add the source under `tool/` with its own license and build notes; or
   - *Not available:* "The PriS-Tool (2010) was a Java research prototype. Its source code is no longer
     maintained and is not publicly available; its functionality is described in Kalloniatis et al. (2010)."
4. **BPMN fragments.** If the BPMN 2.0 files of the Privacy Process Patterns still exist, add them to
   `patterns/bpmn/` (one `<pattern>.bpmn` each). Ideally also add the generic (non-instantiated) textual
   patterns as `patterns/<pattern>.pattern.json` and run `python tools/validate.py`. If the files no
   longer exist, say so in `patterns/bpmn/README.md` and in the Data Availability statement.
5. **Choose licenses** and add a `LICENSE` file (Zenodo asks for one at upload).
6. **Publish:** push to GitHub, enable the repository in Zenodo's GitHub integration, then create a
   release `v1.0.0`. Zenodo mints a DOI for the release.
7. **Insert the DOI** in `README.md`, `CITATION.cff`, the manuscript (Section 7.3 and the Data/Code
   Availability statements) and the response letter.
8. Run `python tests/run_tests.py` one last time; the GitHub Action does the same on every push.
