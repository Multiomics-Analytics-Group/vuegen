set -e
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook

vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/html -rt html
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/pdf -rt pdf
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/docx -rt docx
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/odt -rt odt
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/revealjs -rt revealjs
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/pptx -rt pptx
vuegen -dir docs/example_data/Basic_example_vuegen_demo_notebook -output_dir tests/report_examples/Basic_example_vuegen_demo_notebook/jupyter -rt jupyter

# all of the above quarto based reports, can be opened from the command line with:
# open tests/report_examples/Basic_example_vuegen_demo_notebook/pdf/quarto_report/quarto_report.pdf

cd docs
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -output_dir ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -output_dir ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg/html -rt html
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -output_dir ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg/pdf -rt pdf

# update bot example
vuegen -c example_config_files/Chatbot_example_config.yaml -output_dir ../tests/report_examples/chat_bot
