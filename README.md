# PriS JSON: schemas and examples for machine-readable PriS models

[![DOI](https://zenodo.org/badge/DOI/[ZENODO-DOI].svg)](https://doi.org/[ZENODO-DOI])

Companion repository to the article **"[MANUSCRIPT TITLE]"**, *[JOURNAL]* ([YEAR]).

PriS (Privacy Safeguard) is a goal-oriented privacy requirements engineering method. It links privacy
goals to the organisational goals and business processes they affect, to the Privacy Process Patterns
applied to those processes, and to candidate Privacy Enhancing Technologies (PETs). Earlier work
(Diamantopoulou et al., 2017) proposed JSON templates for these concepts. This repository turns those
templates into **JSON Schemas (draft 2020-12)**, provides the **Career Office example** used in the
article as validating instances, and adds a **validator** with consistency checks.

## Contents

| Path | What it is | Manuscript |
| --- | --- | --- |
| `schema/pris-privacy-requirement.schema.json` | Schema for a privacy-requirement record | Listing 1 |
| `schema/pris-privacy-process-pattern.schema.json` | Schema for the textual part of a Privacy Process Pattern | Listing 2 |
| `templates/` | The two published templates, verbatim (documentation only, not validated) | Listings 1–2 |
| `examples/career-office/anonymity-P4.3.requirement.json` | Anonymity requirement on goal G3.3 and subprocess P4.3 | Listing 3 |
| `examples/career-office/anonymity.pattern.json` | Anonymity pattern instantiated for the Career Office | Listing 4 |
| `patterns/bpmn/` | Place for BPMN 2.0 process fragments of the patterns | Section 5 |
| `tools/validate.py` | Schema validation plus consistency checks | Section 7.3 |
| `tests/` | Self-tests, including invalid files that must be rejected | – |

## Quick start

```bash
pip install -r requirements.txt     # jsonschema >= 4.18
python tools/validate.py            # validates examples/ and patterns/
python tests/run_tests.py           # self-tests
```

To validate your own models, name files `*.requirement.json` or `*.pattern.json` and pass them (or their
folder) to the validator:

```bash
python tools/validate.py my-models/
```

The schemas also work with any draft 2020-12 validator (e.g. `ajv` with `--spec=draft2020`, or VS Code's
`json.schemas` setting).

## What the validator checks

JSON Schema covers structure and vocabulary: required fields, the nine PriS privacy properties, AND/OR
decomposition types and `Option N` keys. `tools/validate.py` adds three checks that JSON Schema cannot
express:

1. `Option N` keys start at 1 and are consecutive.
2. A pattern does not list itself in `Related patterns`.
3. Every PET chosen for a privacy requirement is one of the implementation techniques of the pattern
   applied to its process. The manuscript describes the PET field as the subset of the pattern's
   techniques suited to the specific goal and context. This check runs when the pattern's file is
   validated in the same run.

## Design decisions

- **Faithful to the published templates.** Property names keep their spaces and capitalisation
  (`"privacy requirement"`, `"Organisational Goal"`), and alternatives stay as `"Option 1"`,
  `"Option 2"`, … objects rather than arrays. Existing PriS JSON files therefore validate unchanged.
- **Controlled vocabulary.** `Privacy Goal`, `Process Pattern`, pattern `Name` and `Related patterns`
  take one of nine values: Identification, Authentication, Authorisation, Data Protection, Anonymity,
  Pseudonymity, Unlinkability, Undetectability, Unobservability (British spelling, as in the article).
- **Empty string = not applicable.** A leaf goal has `"Child Goal": ""`, as in the published examples.

## Known limitations (inherited from the v1.0 templates)

These are deliberate in v1.0, to stay compatible with the published templates. They are candidates for a
v2.0 schema (research direction D2 in Table 3 of the article).

- A goal or process records a single child, although PriS goal models allow several.
- A process carries a single `Process Pattern`, although PriS may combine patterns for one process.
- Elements have titles but no separate identifiers, so cross-references rely on matching titles.
- There are no fields for regulatory sources, GDPR stakeholders or compliance evidence (the
  GDPR-oriented PriS framework).

## Provenance

The example files are **illustrative**. `anonymity-P4.3.requirement.json` is adapted from the Career
Office case study in [CONFIRM: Diamantopoulou et al., 2017 / Kalloniatis, 2017].
`anonymity.pattern.json` is a reconstruction of the Anonymity Privacy Process Pattern based on
Diamantopoulou et al. (2017). Neither is an original machine-readable artefact from those studies.

**Not included:** [PriS-Tool availability statement – see RELEASE-CHECKLIST.md].

## How to cite

Please cite the article and this repository; see `CITATION.cff` or the Zenodo record
([ZENODO-DOI]).

## References

- Diamantopoulou, V., Kalloniatis, C., Gritzalis, S., Mouratidis, H.: Supporting privacy by design using
  privacy process patterns. In: ICT Systems Security and Privacy Protection (IFIP SEC 2017), IFIP AICT
  vol. 502, pp. 491–505. Springer (2017). https://doi.org/10.1007/978-3-319-58469-0_33
- Kalloniatis, C.: Incorporating privacy in the design of cloud-based systems: a conceptual meta-model.
  Information & Computer Security 25(5), 614–633 (2017). https://doi.org/10.1108/ICS-06-2016-0044
- Kalloniatis, C., Kavakli, E., Gritzalis, S.: Addressing privacy requirements in system design: the PriS
  method. Requirements Engineering 13(3), 241–255 (2008). https://doi.org/10.1007/s00766-008-0067-3

## License

[CHOOSE BEFORE RELEASE – e.g. CC BY 4.0 for schemas and examples, MIT for `tools/` and `tests/`]
