# Tygron QGIS Plugin

Seamlessly integrate the **Tygron Platform** with **QGIS**. This plugin allows you to stream environmental data layers directly into your GIS environment and perform live edits on project geometries using WFS-T.

This plugin is offered as-is, under the MIT license. This plugin is not part of the core Tygron Platform technology.

This plugin is currently in BETA, and is developed as a first demonstration of the possibilities of an integration between QGIS and the Tygron Platform. Please feel free to use it as an inspiration for your own use cases. 

---

## Installation

Follow these steps to manually add the plugin to your QGIS directory:

1. **Download** the ZIP file found under [Releases].
2. **Within QGIS** navigate to [Plugins] -> [Manage and Install Plugins] -> [Install from ZIP] and select the downloaded file.

You may need to restart the application.


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

* Time based overlays from Tygron will be mapped to the QGIS Temporal Controller and can be played in sequence, it is recommended to set the Stepping Method to [Source Timestamps]

* You can disable the Python Macro Prompt by 
