# Custom writer

Example shows how corsair can be used for custom file generation.

## File structure

- `regmap.json` - register map description file; source for the all generated files
- `csv.j2` - Jinja2 template for CSV files
- `rmap.csv` - generated CSV file

## Artifacts generation

Use

```bash
python3 custom.py
```

to regenerate output CSV file.
