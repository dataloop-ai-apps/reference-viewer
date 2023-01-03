# Reference Viewer

  <img height="40mm" src="https://mk0dataloop4fni44fjg.kinstacdn.com/wp-content/uploads/2020/03/logo.svg">

---

  <img src="./docs/example.png">

---
## Description

The Reference Viewer application enables annotators to view other items in a draggable, resizable window (A.K.A Floating Window) while annotating in the studio.

## Supported mimetypes
* `image/*`
* `application/pdf`


## Installation
* Clone the repository -  `git clone https://github.com/dataloop-ai-apps/reference-viewer.git`
* `cd reference-viewer`
* Publish the app -  `dlp app publish --project-name <PROJECT_NAME>`
* Install - `dlp app install --dpk-id <DPK ID> --project-name <PROJECT_NAME>`

## Application Usage in the Platform
To use the Reference Viewer in an item, edit the item's Metadata and add a modalitiy of type "preview" as follows:
``` json
"modalities": [{
    "ref": "63b42ec7f0d95bdf257c5f8f",
    "type": "preview",
    "mimetype": "image/png",
    "stream": "https://gate.dataloop.ai/api/v1/items/63b42ec7f0d95bdf257c5f8f/stream"
}]
```

  <img src="./docs/metadata.png">

## Contributions, Bugs and Issues - How to Contribute  
We welcome anyone to help us improve this app.  
[Here's](CONTRIBUTING.md) a detailed instructions to help you open a bug or ask for a feature request