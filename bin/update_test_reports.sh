set -e
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook

vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/html -r html
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/pdf -r pdf
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/docx -r docx
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/odt -r odt
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/revealjs -r revealjs
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/pptx -r pptx
vuegen -d docs/example_data/Basic_example_vuegen_demo_notebook -o tests/report_examples/Basic_example_vuegen_demo_notebook/jupyter -r jupyter

# all of the above quarto based reports, can be opened from the command line with:
# open tests/report_examples/Basic_example_vuegen_demo_notebook/pdf/quarto_report/quarto_report.pdf

cd docs
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -o ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -o ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg/html -r html
vuegen -c example_config_files/Basic_example_vuegen_demo_notebook_config.yaml -o ../tests/report_examples/Basic_example_vuegen_demo_notebook_cfg/pdf -r pdf

# update bot example
vuegen -c example_config_files/Chatbot_example_config.yaml -o ../tests/report_examples/chat_bot
