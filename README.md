# Blender Utils

This repository contains a collection of utilities for [Blender](https://www.blender.org/) designed to automate tasks for both GUI and script development.

## Features

- Import additional modules (e.g., torch) into Blender's bundled Python environment in a non-invasive way
- GUI utilities for some common operations (e.g., clearing the workspace, quickly toggling modes)
- Shortcut for animation retargeting (powered by Auto-Rig Pro)
- A variety of helper methods to streamline script development

## Usage

### As Blender Add-on

Download the `zip` file from [Releases](https://github.com/jasongzy/blender_utils/releases) and install it as an add-on within Blender.

After installation, access the add-on via the `Utils` tab in the sidebar of `3D Viewport`.

The path of additional modules can be configured in the add-on preference page.

### As Python Module

This module can work along with standalone [bpy](https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html) in any Python environment. In this case, only `src/bu.py` is installed.

To install:

```shell
pip install bpy
pip install fake-bpy-module  # Recommended for development
pip install git+https://github.com/jasongzy/blender_utils
```

Example usage:

```python
import bpy
import bu

bu.remove_all()
```
