## Case studies

VueGen’s functionality is demonstrated through two case studies:

**1. Predefined Directory**

This introductory case study uses a predefined directory with plots, dataframes, Markdown, and HTML components. Users can generate reports in different formats and modify the configuration file to customize the report structure.

🔗 [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Multiomics-Analytics-Group/vuegen/blob/main/docs/vuegen_basic_case_study.ipynb)

:::{NOTE}
The [configuration file](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/Basic_example_vuegen_demo_notebook_config.yaml) is available in the `docs/example_config_files` folder, and the [directory](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_data/Basic_example_vuegen_demo_notebook) with example data is in the `docs/example_data` folder.
:::


**2. Earth Microbiome Project Data**

This advanced case study demonstrates the application of VueGen in a real-world scenario using data from the [Earth Microbiome Project (EMP)](https://earthmicrobiome.org/). The EMP is an initiative to characterize global microbial taxonomic and functional diversity. The notebook process the EMP data, create plots, dataframes, and other components, and organize outputs within a directory to produce reports. Report content and structure can be adapted by modifying the configuration file. Each report consists of sections on exploratory data analysis, metagenomics, and network analysis.

🔗 [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Multiomics-Analytics-Group/vuegen/blob/main/docs/vuegen_case_study_earth_microbiome.ipynb)

:::{NOTE}
The EMP case study is available online as [HTML](https://multiomics-analytics-group.github.io/vuegen/) and [Streamlit](https://earth-microbiome-vuegen-demo.streamlit.app/) reports.
The [configuration file](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/Earth_microbiome_vuegen_demo_notebook_config) is available in the `docs/example_config_files` folder, and the [directory](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_data/Earth_microbiome_vuegen_demo_notebook) with example data is in the `docs/example_data` folder.
:::


**3. ChatBot Component**

This case study highlights VueGen’s capability to embed a chatbot component into a report subsection, 
enabling interactive conversations inside the report.

Two API modes are supported:

- **Ollama-style streaming chat completion**
If a `model` parameter is specified in the config file, VueGen assumes the chatbot is using Ollama’s [/api/chat endpoint](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion). 
Messages are handled as chat history, and the assistant responses are streamed in real time for a smooth and responsive experience. 
This mode supports LLMs such as `llama3`, `deepsek`, or `mistral`. 

:::{TIP}
See [Ollama’s website](https://ollama.com/) for more details.
:::


- **Standard prompt-response API**
If no `model` is provided, VueGen uses a simpler prompt-response flow. 
A single prompt is sent to an endpoint, and a structured JSON object is expected in return.
Currently, the response can include:
  - `text`: the main textual reply
  - `links`: a list of source URLs (optional)
  - `HTML content`: an HTML snippet with a Pyvis network visualization (optional)

This response structure is currently customized for an internal knowledge graph assistant, but VueGen is being actively developed 
to support more flexible and general-purpose response formats in future releases.

:::{NOTE}
You can see a [configuration file example](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/Chatbot_example_config.yaml) for the chatbot component in the `docs/example_config_files` folder.
:::
