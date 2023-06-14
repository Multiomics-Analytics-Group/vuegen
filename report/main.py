import os
import report as r

if __name__ == '__main__':
    with open(os.path.join('example_data', 'barplot.json'), 'r') as bf:
        plotly_code1 = bf.read()
    with open(os.path.join('example_data', 'lineplot.json'), 'r') as lf:
        plotly_code2 = lf.read()
    
    report = r.Report(1213412, "test_report", 'DOES it WoRK', "Just a test", sections=[])
    section1 = r.Section(21324, "Proteomics", "This is a Proteomics example", "Not much", plots=[])
    section2 = r.Section(24324, "Transcriptomics", "This is a Transcriptomics example", "Not much", plots=[])
    plot1 = r.Plot(3323, "plot1", "plotly", "Test 1", "", plotly_code1)
    plot2 = r.Plot(3423, "plot2", "plotly", "Test 2", "", plotly_code2)
    section1._plots.extend([plot1, plot2])
    section2._plots.extend([plot1, plot2])
    report._sections.extend([section1, section2])
    
    report_gui = r.StreamlitReport(12312, "MyPage", columns=None, report=report)
    report_gui.generate_report(output_dir="tmp")
    report_gui.run_report(output_dir='tmp')
    