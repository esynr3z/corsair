# Simple CSR map

Simple example shows how corsair's output artifacts looks like.

By default, register map with AXI-Lite interface is created. Use `lb_bridge.type` parameter inside `regmap.json` to change this.

## File structure

- `regmap.json` - register map description file; source for the all generated files
- `axil2lb_regs.v`, `regs.v` - generated bridge to convert AXi-Lite to LocalBus transaction and register map itself
- `rmap.md`, `rmap_img` - generated documentation for the register map

## Artifacts generation

Use

```bash
corsair -r regmap.json --hdl --lb-bridge --docs
```

to regenerate all the artifacts with corsair.
