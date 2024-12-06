### Questions
#### Is the UML diagram ok? Should I change or add something?
Ok
Add part to explain that UI is not mandatory
Add subsection class

#### Should I assume that the user already has the plot files? No option for creating the plots from the data?

Yes, the previous part will be done by VCore

#### Should I create a class to validate the integrity of files and yaml, or this can be done inside the corresponding classes? 

No, the validation will be done internally, as a method of the metadataTranslator class

#### Should I create a specific class for handling potential errors? or it will be a repetition of the validation one?

No, it should be done inside every function with try and catch statements or others

#### What do you think about creating a ReportViewFactory, which decides what format is going to be used?

Right now, not necessary, just try the interface approach and then will see

#### Should I also have a Datahandler class, connecting from the UI to the Report?

Not necessary, this is already covered by the MetadataTranslator 

#### Should I have a ReportFormatter class instead of the specific ReporterViews?

No, just work with the interface approach

#### Is it ok if I use the @dataclass decorator to the classes to add dunder/special methods, instead of defining them myself every time?

Ok

#### How the GraphRAG interface can be created using report_generator? Should we add more functionalities later, or implement them now?

It won't be necessarily implemented using report_generator, but some of the functions to visualize graphs or others can be used. 

Also, maybe it's possible to provide the code or other information as input, and then create the specific parts in the report, but this will be evaluated after

#### How we would integrate the network analysis and exporting part into report_generator?

No needed now

#### When to use setuptools library and setup.py script instead of ve managers like pienv or poetry?

Yeah different, setup.py for creating Python package

#### Quarto vs Pandoc

* Quarto is built on pandoc and can convert to many formats, should we rely on its CLI?
* Python wrapper for pandoc - pypandoc
* Another option could be to use jupyter notebooks and from there export the other formats using nbconvert
* Maybe make integration with Quarto or Pandoc optional, and other functionalities working without them

| **Feature**                         | **Pandoc**                                                   | **Quarto**                                                                   |
| ----------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **Supported Formats**               | Wide range, but mostly document-centric (PDF, HTML, Jupyter) | Same formats as Pandoc but more convenient for reports with code execution.  |
| **Multi-format Outputs**            | Requires configuring multiple templates for each format.     | Designed for multi-format publishing from a single `.qmd` file.              |
| **Code Execution**                  | Possible, but not natively integrated.                       | Native support for embedded executable code (Python, R, Julia).              |
| **Custom Templates**                | Requires manual setup (LaTeX, Markdown, etc.).               | Pre-defined templates and easy-to-customize options.                         |
| **Ease of Use for Complex Reports** | Basic transformation, might need more manual work.           | Streamlined for complex reports with multiple sections, metadata, and plots. |
| **Integration with Jupyter**        | Can convert Jupyter Notebooks to other formats.              | Native integration with Jupyter Notebooks (supports notebooks as input).     |

#### Learning/Doing
* OOP in Python
* UML and conventions
* Design patterns
* Streamlit and St components - how it works under the hood 
* LLM course - how to create RAGs

#### Extra
Add sub-sections for grouping plots of a certain category together




