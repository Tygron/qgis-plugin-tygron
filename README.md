# Tygron QGIS Plugin

Seamlessly integrate the **Tygron Platform** with **QGIS**. This plugin allows you to stream environmental data layers directly into your GIS environment and perform live edits on project geometries using WFS-T.

---

## Installation

Follow these steps to manually add the plugin to your QGIS directory:

1. **Download** the ZIP file containing the source code.
2. **Extract** the contents into a folder.
3. **Move** that folder to the following directory:
> `C:\Users\[YourUser]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`



---

## Opening a Project

To interact with a Tygron project, you need to authenticate via a **Session API Key**.

### 1. Find your API Key

* Open or create a project in the **Tygron Platform Client**.
* In the editor, navigate to the **Tools** tab at the top of the window.
* Click on **API Overview**. This will open a new tab in your web browser.
* Find and **Copy** the API Session Key (displayed in bold text).

### 2. Connect to QGIS

* Open QGIS and launch the Tygron Plugin.
* **Paste** the copied key into the plugin window to enter your session.

### 3. Import Project

* It is recommended to start by doing a generic import of your project data.
* Once connected to the session, select "Import Project", the following data will be loaded in:
- Standard Map
- Buildings
- Neighborhoods
- Areas
- Terrain

* You may import any overlays from your project by navigating to Overlays, and selecting any layer you'd like to import.