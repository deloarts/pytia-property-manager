# sample files

Explains the config of all sample files.

All sample files must be copied, renamed and edited to fit your needs.

## 1 settings.sample.json

This file contains the basic settings for the app.

- **Location**: [/pytia_property_manager/resources/settings.sample.json](../pytia_property_manager/resources/settings.sample.json)
- **Rename to**: `settings.json`

### 1.1 file content

```json
{
    "title": "PYTIA Property Manager",
    "debug": false,
    "demo": false,
    "revision": 0,
    "restrictions": {
        "allow_all_users": true,
        "allow_all_editors": true,
        "allow_unsaved": true,
        "allow_outside_workspace": true,
        "strict_project": false,
        "strict_machine": false,
        "enable_information": true
    },
    "separators": {
        "bought": " - ",
        "metadata": " -- "
    },
    "nomenclature": {
        "made": "MACHINE-ASSEMBLY-PART",
        "bought": "NAME - ORDER NUMBER - MANUFACTURER"
    },
    "processes": {
        "first": 1,
        "min": 3,
        "max": 6
    },
    "tolerances": [
        "ISO 2768 1-m 2-K",
        "ISO 2768 1-f 2-K",
        "ISO 2768 1-c 2-K",
        "ISO 2768 1-v 2-K"
    ],
    "spare_part_level": [
        "None",
        "Reserve",
        "Annual"
    ],
    "paths": {
        "catia": "C:\\CATIA\\V5-6R2017\\B27",
        "material": "C:\\pytia\\material",
        "local_dependencies": "C:\\pytia\\local_deps",
        "release": "C:\\pytia\\release"
    },
    "files": {
        "app": "pytia_property_manager.pyz",
        "launcher": "pytia_property_manager.catvbs",
        "bounding_box_launcher": "pytia_bounding_box.catvbs",
        "material": "Material.CATMaterial",
        "workspace": "workspace.yml"
    },
    "urls": {
        "help": null
    },
    "mails": {
        "admin": "admin@company.com"
    }
}
```

### 1.2 description

name | type | description
--- | --- | ---
title | `str` | The apps title. This will be visible in the title bar of the window.
debug | `bool` | The flag to declare the debug-state of the app. The app cannot be built if this value is true.
demo | `bool` | The flag to declare the demo-state of the app. If set to `true` only the UI will be loaded, and no connection to CATIA will be established.
revision | `int` | The starting revision for a document. Can be any number or a letter `a-z` or `A-Z`.
restrictions.allow_all_users | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users from the **users.json** file can modify the properties.
restrictions.allow_all_editors | `bool` | If set to `true` any user can make changes to the documents properties. If set to `false` only those users which are declared in the **workspace** file can modify the properties. If no workspace file is found, or no **editors** list-item is inside the workspace file, then this is omitted, and everyone can make changes.
restrictions.allow_unsaved | `bool` | If set to `false` an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.allow_outside_workspace | `bool` | If set to `false` a **workspace** file must be provided somewhere in the folder structure where the document is saved. This also means, that an unsaved document (a document which doesn't have a path yet) cannot be modified.
restrictions.strict_project | `bool` | If set to `true` the project number must be present in the **workspace** file, otherwise the changes to the properties cannot be saved. If no workspace file is found, or no **projects** list-item is inside the workspace file, then this is omitted, and any project number can be written to the documents properties.
restrictions.strict_machine | `bool` | If set to `true` the machine number must be present in the **workspace** file, otherwise the changes to the properties cannot be saved. If no workspace file is found, or no **machine** item is inside the workspace file, then this is omitted, and any machine number can be written to the documents properties. Further, if set to `true`, an existing machine number (a value that is already present in the documents properties) will be overwritten with the value from the workspace file.
restrictions.enable_information | `bool` | If set to `true` the user will see the notifications from the **information.json** file.
separators.bought | `str` | The separator that is used for the bought nomenclature.
separators.metadata | `str` | The separator that is used to distinguish the metadata from the name of a material.
nomenclature.made | `str` | The nomenclature for made parts or products.
nomenclature.bought | `str` | The nomenclature for bought parts or products.
processes.first | `int` | The index of the first process. Can be 0 or 1.
processes.min | `int` | The minimum amount of processes to display in the UI.
processes.max | `int` | The maximum amount of processes to display in the UI.
tolerances | `List[str]` | A list of available tolerances.
spare_part_level | `List[str]` | A list of available spare part levels.
paths.catia | `str` | The absolute path to the CATIA executables.
paths.material | `str` | The absolute path to the CATMaterial file.
paths.local_dependencies | `str` | The folder where local local_dependencies (python wheel files) for the installer are stored.
paths.release | `str` | The folder where the launcher and the app are released into.
files.app | `str` | The name of the released python app file.
files.launcher | `str` | The name of the release catvbs launcher file.
files.bounding_box_launcher | `str` | The filename of the launcher for the bounding box app (must be stored in the `paths.release` folder).
files.material | `str` | The filename of CATMaterial file.
files.workspace | `str` | The name of the workspace file.
urls.help | `str` or `null` | The help page for the app. If set to null the user will receive a message, that no help page is provided.
mails.admin | `str` | The mail address of the sys admin. Required for error mails.

## 2 users.sample.json

This file contains a list of users known to the system.

- **Location**: [/pytia_property_manager/resources/users.sample.json](../pytia_property_manager/resources/users.sample.json)
- **Rename to**: `users.json`

### 2.1 file content

```json
[
    {
        "logon": "admin",
        "id": "001",
        "name": "Administrator",
        "mail": "admin@company.com"
    },
    ...
]
```

### 2.2 description

name | type | description
--- | --- | ---
logon | `str` | The windows logon name of the user.
id | `str` | The ID of the user. Can be used for the employee ID.
name | `str` | The name of the user.
mail | `str` | The users mail address.
