SingingGadgets
================

This is a Python singing synthesis API wrapped at low-level.

## Relationship with ScoreDraft

I've been developing [ScoreDraft](https://github.com/fynv/ScoreDraft) for some time. 
There are some limitations of ScoreDraft due to its architecture.
The new project SingingGadgets is to started to address these issues.

ScoreDraft is basically a plug-in structured C++ project with a Python shell at its outmost layer, using Python merely as its UI. Such architecture is designed for end users to use ScoreDraft directly to author music. 

However, some technically user tells me that they need some Python modules as building blocks to build their own singing synthesis systems, and I have to tell them, ScoreDraft is not suitable for such purpose. And now, SingingGadgets is coming to fulfill such requirements.

The reason why ScoreDraft is not suitable to be used as a building block is:

1. Low-level wave-form processing are all encapsulated within C++ modules with no direct access from Python
2. The deployment of ScoreDraft requires an independent folder with C++ modules and data files organized in a specific form, much like a windows application. In other word, it cannot be naturally integrate into the Python ecosystem.

SingingGadgets, on the other hand, is organized as a package of standard Python modules that can be seamlessly integrated to your Python ecosystem. It assumes no relative paths to the application data, and leaves the decision to application layer. In SingingGadgets, I try to use Python provided data structures, such as "bytes" when ever possible, so that it will be possible to communicate with other Python libraries.

If it goes smoothly, I will in the end restructure ScoreDraft based on this library, thus exposing both high-level and low-level Python APIs. The existing ScoreDraft will be kept in another branch, because its C++ flavor design might be a little more efficient in speed.
