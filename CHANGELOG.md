# Release Notes

All notable changes to this project are documented in this file. It was automatically generated with
the [changelog-from-release](https://github.com/rhysd/changelog-from-release) tool.

<a id="v0.6.0"></a>
# [v0.6.0 (relax dependency pinning)](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.6.0) - 2026-02-10

Maintenance release, which might break workflows as the pinned versions are gone.

## What's Changed
* :wrench: loosen versions by [@enryH](https://github.com/enryH) in [#166](https://github.com/Multiomics-Analytics-Group/vuegen/pull/166)
* 🚧 update runner images by [@enryH](https://github.com/enryH) in [#170](https://github.com/Multiomics-Analytics-Group/vuegen/pull/170)
* :art: format with latest black version by [@enryH](https://github.com/enryH) in [#172](https://github.com/Multiomics-Analytics-Group/vuegen/pull/172)
* :memo: start FAQ section by [@enryH](https://github.com/enryH) in [#171](https://github.com/Multiomics-Analytics-Group/vuegen/pull/171)


**Full Changelog**: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.5.1...v0.6.0

[Changes][v0.6.0]


<a id="v0.5.1"></a>
# [v0.5.1](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.5.1) - 2025-09-23

## What's Changed
* 📝 Update readme and small logo by [@sayalaruano](https://github.com/sayalaruano) in [#158](https://github.com/Multiomics-Analytics-Group/vuegen/pull/158)
* Fix App: Exact Python version and local exec by [@enryH](https://github.com/enryH) in [#153](https://github.com/Multiomics-Analytics-Group/vuegen/pull/153)
* 📝 Upate CONTRIBUTING.md file and create PR template by [@sayalaruano](https://github.com/sayalaruano) in [#163](https://github.com/Multiomics-Analytics-Group/vuegen/pull/163)
* 📝 Docs: Create and update CHANGELOG.md using changelog-from-release by [@sayalaruano](https://github.com/sayalaruano) in [#164](https://github.com/Multiomics-Analytics-Group/vuegen/pull/164)
* 📝 Create makefile to automate docs building process by [@sayalaruano](https://github.com/sayalaruano) in [#165](https://github.com/Multiomics-Analytics-Group/vuegen/pull/165)


[Changes][v0.5.1]


<a id="v0.5.0"></a>
# [v0.5.0](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.5.0) - 2025-07-19

## Bundled GUI

Release `0.5.0` bundled GUI was built using Python 3.12.10.

```
conda create -n vuegen_gui pip python=3.12.10 jupyter
```

## What's Changed
* 📝 Update installation instruction for conda by adding conda-forge channel by [@sayalaruano](https://github.com/sayalaruano) in [#122](https://github.com/Multiomics-Analytics-Group/vuegen/pull/122)
* 📝 Add apicall and chatbot notebooks by [@sayalaruano](https://github.com/sayalaruano) in [#123](https://github.com/Multiomics-Analytics-Group/vuegen/pull/123)
* :zap: only build GUI on push to main, releases and manuel triggers by [@enryH](https://github.com/enryH) in [#130](https://github.com/Multiomics-Analytics-Group/vuegen/pull/130)
* Check that report files are unchanged (for now in streamlit) by [@enryH](https://github.com/enryH) in [#132](https://github.com/Multiomics-Analytics-Group/vuegen/pull/132)
* 🐛 Make excel df paths relative instead of absolute by [@sayalaruano](https://github.com/sayalaruano) in [#134](https://github.com/Multiomics-Analytics-Group/vuegen/pull/134)
* :bug: allow to specify output folder - use only relative paths by [@enryH](https://github.com/enryH) in [#136](https://github.com/Multiomics-Analytics-Group/vuegen/pull/136)
* :construction: start to explore adding subsections to homesection by [@enryH](https://github.com/enryH) in [#125](https://github.com/Multiomics-Analytics-Group/vuegen/pull/125)
* Style and format codebase by [@enryH](https://github.com/enryH) in [#131](https://github.com/Multiomics-Analytics-Group/vuegen/pull/131)
* :bug: use dynamic version to display version. by [@enryH](https://github.com/enryH) in [#142](https://github.com/Multiomics-Analytics-Group/vuegen/pull/142)
* 📝 Update logo and citation by [@sayalaruano](https://github.com/sayalaruano) in [#145](https://github.com/Multiomics-Analytics-Group/vuegen/pull/145)
* :sparkles: shell script to update the tests by [@enryH](https://github.com/enryH) in [#148](https://github.com/Multiomics-Analytics-Group/vuegen/pull/148)
* :sparkles: make relative outputs and path work better in streamlit by [@enryH](https://github.com/enryH) in [#146](https://github.com/Multiomics-Analytics-Group/vuegen/pull/146)
* :sparkles: do not fail silently - fail build by [@enryH](https://github.com/enryH) in [#149](https://github.com/Multiomics-Analytics-Group/vuegen/pull/149)
* Load home image on the base folder when creating a report from a directory by [@sayalaruano](https://github.com/sayalaruano) in [#152](https://github.com/Multiomics-Analytics-Group/vuegen/pull/152)
* :bug: update formatting to support again multi-line descriptions by [@enryH](https://github.com/enryH) in [#151](https://github.com/Multiomics-Analytics-Group/vuegen/pull/151)

[Changes][v0.5.0]


<a id="v0.4.1"></a>
# [v0.4.1](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.4.1) - 2025-05-22

## What's Changed
* Update GUI installation instructions by [@enryH](https://github.com/enryH) in [#118](https://github.com/Multiomics-Analytics-Group/vuegen/pull/118)
* Streamlit and quarto relative paths, and fix plots resizing by [@sayalaruano](https://github.com/sayalaruano) in [#119](https://github.com/Multiomics-Analytics-Group/vuegen/pull/119)
* Use multiple sheets from an excel file in reports by [@enryH](https://github.com/enryH) in [#115](https://github.com/Multiomics-Analytics-Group/vuegen/pull/115)

[Changes][v0.4.1]


<a id="v0.4.0"></a>
# [v0.4.0](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.4.0) - 2025-05-06

## What's Changed
* :bug: pass config path to completion message by [@enryH](https://github.com/enryH) in [#111](https://github.com/Multiomics-Analytics-Group/vuegen/pull/111)
* :sparkles: Shut down button for streamlit app by [@enryH](https://github.com/enryH) in [#113](https://github.com/Multiomics-Analytics-Group/vuegen/pull/113)
* Split readme docs by [@sayalaruano](https://github.com/sayalaruano) in [#114](https://github.com/Multiomics-Analytics-Group/vuegen/pull/114)
* Make required folder structure more flexible by [@enryH](https://github.com/enryH) in [#108](https://github.com/Multiomics-Analytics-Group/vuegen/pull/108)
* Recursive sub-sub-sections components by [@enryH](https://github.com/enryH) in [#112](https://github.com/Multiomics-Analytics-Group/vuegen/pull/112)
* Ruff checks by [@enryH](https://github.com/enryH) in [#117](https://github.com/Multiomics-Analytics-Group/vuegen/pull/117)
* Update documentation (minor) by [@enryH](https://github.com/enryH) in [#83](https://github.com/Multiomics-Analytics-Group/vuegen/pull/83)

[Changes][v0.4.0]


<a id="v0.3.3"></a>
# [v0.3.3](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.3.3) - 2025-04-16

## What's Changed
* 📝 Docs: change text from logo to path to avoid changes across OS by [@sayalaruano](https://github.com/sayalaruano) in [#106](https://github.com/Multiomics-Analytics-Group/vuegen/pull/106)
* 🚧 ensure a valid python identifier for report_manger.py streamlit file by [@enryH](https://github.com/enryH) in [#105](https://github.com/Multiomics-Analytics-Group/vuegen/pull/105)
* 🤖 Api and chatbot components update by [@sayalaruano](https://github.com/sayalaruano) in [#107](https://github.com/Multiomics-Analytics-Group/vuegen/pull/107)

[Changes][v0.3.3]


<a id="v0.3.2"></a>
# [v0.3.2](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.3.2) - 2025-04-01

## What's Changed
* 🐛 Fix: change the engine to export tables to images from chrome to matplotlib by [@sayalaruano](https://github.com/sayalaruano) in [#104](https://github.com/Multiomics-Analytics-Group/vuegen/pull/104)

[Changes][v0.3.2]


<a id="v0.3.1"></a>
# [v0.3.1](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.3.1) - 2025-03-26

## What's Changed
* Quarto checks and output directory parameters by [@sayalaruano](https://github.com/sayalaruano) in [#99](https://github.com/Multiomics-Analytics-Group/vuegen/pull/99)

[Changes][v0.3.1]


<a id="v0.3.0"></a>
# [v0.3.0](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.3.0) - 2025-03-21

## What's Changed

* :bug: Save streamlit rand quarto reports with Posix and change str paths to Path by [@enryH](https://github.com/enryH) in [#78](https://github.com/Multiomics-Analytics-Group/vuegen/pull/78)
* Non random import order and separation from setup code by [@enryH](https://github.com/enryH) in [#92](https://github.com/Multiomics-Analytics-Group/vuegen/pull/92)
* Os standalone installers (with a GUI) by [@enryH](https://github.com/enryH) in [#73](https://github.com/Multiomics-Analytics-Group/vuegen/pull/73)
  - includes updates to logging, output-folder specifications, specifying static export folders, itables fix and Windows Path compatibility
  - first GUI created
* 🐛 Fix: add code to handle plotly plots generated with R by [@sayalaruano](https://github.com/sayalaruano) in [#96](https://github.com/Multiomics-Analytics-Group/vuegen/pull/96)
* :art: updadte GUI instructions, format document by [@enryH](https://github.com/enryH) in [#98](https://github.com/Multiomics-Analytics-Group/vuegen/pull/98)

To launch the bundled GUI, you will need to unzip the installer compatible with your system (MacOS with arm64/ apple silicon or x86_64/ intel or Windows x86_64) and run `vuegen_gui` in the unpacked main folder. Most dependencies are included into the bundle using PyInstaller.

Streamlit works out of the box as a purely Python based package. For `html` creation you will have to have a Python 3.12 installation with the `jupyter` package installed as `quarto` needs to start a kernel for execution. This is also true if you install `quarto` globally on your machine.

We recommend using miniforge to install Python and the conda package manager:

- [conda-forge.org/download/](https://conda-forge.org/download/)

We continue our example assuming you have installed the `miniforge` distribution for your machine. now, create a virtual environment:

```bash
conda create -n vuegen_gui -c conda-forge python=3.12 jupyter
conda info -e # find environment location
```

Find the vuegen_gui path for your local `user`.

On **MacOS** you need to add a `bin` to the path:

```bash
/Users/user/miniforge3/envs/vuegen_gui/bin
```

On **Windows** you can use the path as displayed by `conda info -e`:

> [!NOTE]
> On Windows a base installation of miniforge with `jupyter` might work as well as the app can see your entire Path which is not the case on MacOS.

```bash
C:\Users\user\miniforge3\envs\vuegen_gui
```

More information regarding the app and builds can be found in the [GUI README](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/gui/README.md).

[Changes][v0.3.0]


<a id="v0.2.2"></a>
# [v0.2.2](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.2.2) - 2025-02-28

## What's Changed
* No default logger and print message after completion by [@sayalaruano](https://github.com/sayalaruano) in [#76](https://github.com/Multiomics-Analytics-Group/vuegen/pull/76)

[Changes][v0.2.2]


<a id="v0.2.1"></a>
# [v0.2.1](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.2.1) - 2025-02-25

## What's Changed
* Add basic example directory and notebook by [@sayalaruano](https://github.com/sayalaruano) in [#63](https://github.com/Multiomics-Analytics-Group/vuegen/pull/63)
* :art: add basic vuegen demo to docs  [#64](https://github.com/Multiomics-Analytics-Group/vuegen/issues/64) by [@enryH](https://github.com/enryH) in [#65](https://github.com/Multiomics-Analytics-Group/vuegen/pull/65)
* Display dataframes in streamlit apps with aggrid by [@sayalaruano](https://github.com/sayalaruano) in [#66](https://github.com/Multiomics-Analytics-Group/vuegen/pull/66)
* 👷 CI: Add CI steps to create streamlit example branch and deploy EMP … by [@sayalaruano](https://github.com/sayalaruano) in [#70](https://github.com/Multiomics-Analytics-Group/vuegen/pull/70)
* :art: sort imports, format codebase with black by [@enryH](https://github.com/enryH) in [#72](https://github.com/Multiomics-Analytics-Group/vuegen/pull/72)
* Fix dfi library issue to export a dataframe as an image by [@sayalaruano](https://github.com/sayalaruano) in [#74](https://github.com/Multiomics-Analytics-Group/vuegen/pull/74)

[Changes][v0.2.1]


<a id="v0.2.0"></a>
# [v0.2.0](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.2.0) - 2025-02-05

## What's Changed
* 🐛 build docs - fix errors by [@enryH](https://github.com/enryH) in [#49](https://github.com/Multiomics-Analytics-Group/vuegen/pull/49)
* :art: publish report to GitHub Pages by [@enryH](https://github.com/enryH) in [#51](https://github.com/Multiomics-Analytics-Group/vuegen/pull/51)
* Readme and img update by [@sayalaruano](https://github.com/sayalaruano) in [#52](https://github.com/Multiomics-Analytics-Group/vuegen/pull/52)
* :art: add dynamic versioning of python pkg by [@enryH](https://github.com/enryH) in [#50](https://github.com/Multiomics-Analytics-Group/vuegen/pull/50)
* :art: visualize example in docs by [@enryH](https://github.com/enryH) in [#54](https://github.com/Multiomics-Analytics-Group/vuegen/pull/54)
* Update footer img by [@sayalaruano](https://github.com/sayalaruano) in [#53](https://github.com/Multiomics-Analytics-Group/vuegen/pull/53)
* Update demo noteb by [@sayalaruano](https://github.com/sayalaruano) in [#55](https://github.com/Multiomics-Analytics-Group/vuegen/pull/55)

[Changes][v0.2.0]


<a id="v0.1.0"></a>
# [v0.1.0](https://github.com/Multiomics-Analytics-Group/vuegen/releases/tag/v0.1.0) - 2025-01-30

## What's Changed
* Mk_pkg by [@enryH](https://github.com/enryH) in [#30](https://github.com/Multiomics-Analytics-Group/vuegen/pull/30)
* Config generator from a directory by [@sayalaruano](https://github.com/sayalaruano) in [#33](https://github.com/Multiomics-Analytics-Group/vuegen/pull/33)
* :sparkles: basic docs by [@enryH](https://github.com/enryH) in [#32](https://github.com/Multiomics-Analytics-Group/vuegen/pull/32)
* St autorun argument and updated README by [@sayalaruano](https://github.com/sayalaruano) in [#35](https://github.com/Multiomics-Analytics-Group/vuegen/pull/35)
* Entrypoint by [@enryH](https://github.com/enryH) in [#38](https://github.com/Multiomics-Analytics-Group/vuegen/pull/38)
* :zap: only run docs for one python version, save only once by [@enryH](https://github.com/enryH) in [#44](https://github.com/Multiomics-Analytics-Group/vuegen/pull/44)
* EMP case study as example data by [@sayalaruano](https://github.com/sayalaruano) in [#45](https://github.com/Multiomics-Analytics-Group/vuegen/pull/45)
* restructure package layout by [@enryH](https://github.com/enryH) in [#42](https://github.com/Multiomics-Analytics-Group/vuegen/pull/42)
* ➕ Add quarto as default dependency by [@enryH](https://github.com/enryH) in [#46](https://github.com/Multiomics-Analytics-Group/vuegen/pull/46)
* :art: readthedocs configuration by [@enryH](https://github.com/enryH) in [#48](https://github.com/Multiomics-Analytics-Group/vuegen/pull/48)

## New Contributors
* [@enryH](https://github.com/enryH) made their first contribution in [#30](https://github.com/Multiomics-Analytics-Group/vuegen/pull/30)
* [@sayalaruano](https://github.com/sayalaruano) made their first contribution in [#33](https://github.com/Multiomics-Analytics-Group/vuegen/pull/33)

[Changes][v0.1.0]


[v0.6.0]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.5.1...v0.6.0
[v0.5.1]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.5.0...v0.5.1
[v0.5.0]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.4.1...v0.5.0
[v0.4.1]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.4.0...v0.4.1
[v0.4.0]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.3.3...v0.4.0
[v0.3.3]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.3.2...v0.3.3
[v0.3.2]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.3.1...v0.3.2
[v0.3.1]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.3.0...v0.3.1
[v0.3.0]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.2.2...v0.3.0
[v0.2.2]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.2.1...v0.2.2
[v0.2.1]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/Multiomics-Analytics-Group/vuegen/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/Multiomics-Analytics-Group/vuegen/tree/v0.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.9.1 -->
