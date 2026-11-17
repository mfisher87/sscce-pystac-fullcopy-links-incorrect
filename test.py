# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "pystac==1.16.0",
# ]
# ///


"""SSCCE (sscce.org): pystac's `Catalog.full_copy()` drops `extra_fields` on `Link`s.

`Link.clone` (pystac/link.py) rebuilds a link from enumerated fields `rel`, `target`,
`media_type`, and `title` only, so any `extra_fields` are lost.

Other entities and code branches correctly handle deep copies.
E.g. `Asset.clone` (pystac/asset.py) deep-copies its `extra_fields`, and
`Link.from_dict` (pystac/link.py) restores them when a catalog is read back from disk.
"""

import difflib
import json
import sys
import tempfile
from pathlib import Path

import pystac

LINK_EXTRA_FIELDS = {"foo:bar": ["baz"]}


def write_catalog(catalog: pystac.Catalog, *, root_dir: Path) -> str:
    """Save `catalog` under `root_dir` and return its catalog.json as text."""
    catalog.normalize_hrefs(str(root_dir))
    catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
    return (root_dir / "catalog.json").read_text(encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        before_dir = tmpdir / "before" 
        after_dir = tmpdir / "after" 

        catalog = pystac.Catalog(
            id="link-clone-sscce",
            description="Link.clone drops extra_fields",
        )
        catalog.add_link(
            pystac.Link(
                rel="whatever",
                target="./bullseye.parquet",
                media_type=pystac.MediaType.PARQUET,
                extra_fields=LINK_EXTRA_FIELDS,
            ),
        )

        before = write_catalog(catalog, root_dir=before_dir)
        after = write_catalog(catalog.full_copy(), root_dir=after_dir)

    sys.stdout.writelines(
        difflib.ndiff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
        ),
    )

    did_link_survive = "foo:bar" in json.loads(after)["links"][-1]
    print(f"\nextra field foo:bar survived full_copy: {did_link_survive}", file=sys.stderr)
    return 0 if did_link_survive else 1


if __name__ == "__main__":
    raise SystemExit(main())
