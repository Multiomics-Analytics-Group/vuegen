# Report Generator
Generates web interface reports with visualisations


The Report Generator allows you to create web interfaces in an automated manner by defining Reports as collections of Plots divided into Sections (pages).

<p align="center">
  <img src="https://github.com/Multiomics-Analytics-Group/report_generator/assets/1425851/439f4656-25a9-4be7-80d7-67b60e068d2a" width="600">
</p>



For now, the generated reports can run as multi-page [Streamlit](https://streamlit.io/) sharable interfaces but the ReportInterface `class` can be extended to other frontend libraries.

### Installation
``` shell
python setup.py install
```

### Execution Example
``` shell
python report/main.py
```

#### main.py
``` python
import os
import report as r

if __name__ == '__main__':
    # Reading Plotly plots in json format
    with open(os.path.join('example_data', 'barplot.json'), 'r') as bf:
        plotly_code1 = bf.read()
    with open(os.path.join('example_data', 'lineplot.json'), 'r') as lf:
        plotly_code2 = lf.read()

    # Creating a new Report
    report = r.Report(1213412, "test_report", 'DOES it WoRK', "Just a test", sections=[])

    # Creating Sections
    section1 = r.Section(21324, "Proteomics", "This is a Proteomics example", "Not much", plots=[])
    section2 = r.Section(24324, "Transcriptomics", "This is a Transcriptomics example", "Not much", plots=[])

    # Creating Plots
    plot1 = r.Plot(3323, "plot1", "plotly", "Test 1", "", plotly_code1)
    plot2 = r.Plot(3423, "plot2", "plotly", "Test 2", "", plotly_code2)

    # Adding the Plots to the Sections
    section1._plots.extend([plot1, plot2])
    section2._plots.extend([plot1, plot2])
    # Adding the Sections to the Report
    report._sections.extend([section1, section2])

    # Generating a Streamlit interface
    report_gui = r.StreamlitReport(12312, "MyPage", columns=None, report=report)
    report_gui.generate_report(output_dir="tmp")
    report_gui.run_report(output_dir='tmp')
```


