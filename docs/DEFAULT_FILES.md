# default files

Explains the config of all default files.

All default files can be copied, renamed and edited to fit your needs.

## 1 information.default.json

This file contains a list of information, which will be shown to the user when the app has been used `counter` times.

- **Location**: [/pytia_property_manager/resources/information.default.json](../pytia_property_manager/resources/information.default.json)
- **Rename to**: `information.json`

### 1.1 file content

```json
[
    {
        "counter": 5,
        "msg": "If you need help using this app, or if you just want to know more about the available features: Press F1."
    },
    ...
]
```

### 1.2 description

name | type | description
--- | --- | ---
counter | `int` | The amount of app-usages when the information is shown.
id | `str` | The message to show.

## 2 processes.default.json

This file contains a list of processes, which are used to pre-apply a preset.

- **Location**: [/pytia_property_manager/resources/processes.default.json](../pytia_property_manager/resources/processes.default.json)
- **Rename to**: `processes.json`

### 2.1 file content

```json
[
    {
        "name": "Milling",
        "preset": "Standard",
        "metadata_required": false
    },
    {
        "name": "Turning",
        "preset": "Shaft",
        "metadata_required": false
    },
    {
        "name": "Painting",
        "note": "Color: $\nLayers: 2\nLayer-thickness: 150-200µm",
        "metadata_required": true
    },
    ...
]
```

> ✏️ A dollar `$` sign is a placeholder for the material metadata and will be replaced with the metadata, which the user selects via the material manager.

### 2.2 description

name | type | description
--- | --- | ---
name | `str` | The name of the process.
preset | `str` | The name of the preset to apply.
metadata_required | `bool` | If set to **true**, and not metadata-placeholder (the dollar sign) is in the note, the user will receive a warning. If set to **false**, but there is a dollar in the note, the dollar sign will be replaced with a hyphen `-`.

## 3 properties.default.json

This file contains all part properties, which are required for this app.

- **Location**: [/pytia_property_manager/resources/properties.default.json](../pytia_property_manager/resources/properties.default.json)
- **Rename to**: `properties.json`

### 3.1 file content

```json
{
    "infra": {
        "project": "pytia.project",
        "machine": "pytia.machine",
        "material": "pytia.material",
        "base_size": "pytia.base_size",
        "base_size_preset": "pytia.base_size_preset",
        "mass": "pytia.mass",
        "manufacturer": "pytia.manufacturer",
        "supplier": "pytia.supplier",
        "tolerance": "pytia.tolerance",
        "spare_part_level": "pytia.spare_part_level",
        "creator": "pytia.creator",
        "modifier": "pytia.modifier"
    },
    "notes": {
        "general": "pytia.note_general",
        "material": "pytia.note_material",
        "base_size": "pytia.note_base_size",
        "supplier": "pytia.note_supplier",
        "production": "pytia.note_production"
    },
    "production": {
        "process_n": "pytia.process_$",
        "note_process_n": "pytia.note_process_$"
    }
}
```

### 3.2 description

name | type | description
--- | --- | ---
`generic` | `str` | The name of the property, which stores the value of `generic`.
