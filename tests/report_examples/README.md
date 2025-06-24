# Report files as examples and for testing

- the files are used to check for changes in
  the 'CICD Python Package' Action (`cdci.yaml`)
- if there are differences observed, the Action will fail, although the report can
  still be the same which is generated based on the streamlit Python files or `.qmd` files
- if changes are intended, one needs to commit the changnes to this folder

```bash
# main folder of the repository

vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook -rt html
```
