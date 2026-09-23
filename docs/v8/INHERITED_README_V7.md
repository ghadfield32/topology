# Listening to Shape Learning Lab — v7

Open **START_HERE.html** after fully extracting the ZIP. This is the complete retained course plus new beginner entry guides and cross-industry evidence laboratories.

[First session, setup and migration](../v7/START.md) · [15 observed sources and their limits](../v7/DATA_CATALOG.md) · [Coverage](../v7/COVERAGE.md) · [Current verification](../v7/VERIFICATION.md) · [Source audit](../v7/SOURCE_AUDIT.md)

31 core stages; 10 industry cases; 2 new methods laboratories. All saved reference outputs are demonstrations, not learner assessments. Deliberately incomplete functions occur only in separately labeled learner assignments.

```bash
python -m pip install -e ".[notebooks,test,reader]"
python scripts/course_v7.py stage 0
python scripts/course_v7.py check all
python -m pytest -q -ra
python -m jupyterlab
```

Add the physics extra for the retained CPU neural examples: `python -m pip install -e ".[physics]"`. Installation needs network/cache; supplied data do not. Preserve my_work and existing progress logs when migrating. New material is an original extension to the supplied topic outline, not the full forthcoming book text, an author-endorsed course, or professional certification.
