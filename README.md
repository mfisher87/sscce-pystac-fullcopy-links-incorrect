# [SSCCE](https://sscce.org) of pystac `Catalog.full_copy()` dropping fields from `Link`s 

## Usage

```bash
uv run test.py
```

### Expected

No difference in copies of catalog -- link preserved including `extra_fields`.


### Actual

```diff
  {
    "type": "Catalog",
    "id": "link-clone-repro",
    "stac_version": "1.1.0",
    "description": "Link.clone drops extra_fields",
    "links": [
      {
        "rel": "root",
        "href": "./catalog.json",
        "type": "application/json"
      },
      {
        "rel": "whatever",
        "href": "./bullseye.parquet",
-       "type": "application/x-parquet",
?                                      -
+       "type": "application/x-parquet"
-       "foo:bar": [
-         "baz"
-       ]
      }
    ]
```
