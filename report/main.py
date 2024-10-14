import os
import report as r

if __name__ == '__main__':
    with open(os.path.join('example_data', 'barplot.json'), 'r') as bf:
        plotly_code1 = bf.read()
    with open(os.path.join('example_data', 'lineplot.json'), 'r') as lf:
        plotly_code2 = lf.read()
    
    # Create report
    report = r.Report(1213412, "test_report", 'DOES it WoRK', "Just a test", sections=[])
    
    # Create plots
    plot1 = r.Plot(3323, "plot1", "plotly", "Test 1", "", plotly_code1)
    plot2 = r.Plot(3423, "plot2", "plotly", "Test 2", "", plotly_code2)
    
    # Create subsections
    subsection1_prot = r.Subsection(5001, "Subsection 1 Proteomics", "Subsection Example 1", "This is the first prot subsection", plots=[plot1])
    subsection2_prot = r.Subsection(5002, "Subsection 2 Proteomics", "Subsection Example 2", "This is the second prot subsection", plots=[plot2])
    subsection1_trans = r.Subsection(5003, "Subsection 1 Transcriptomics", "Subsection Example 3", "This is the first transcript subsection", plots=[plot1, plot2])
    
    # Create sections and add subsections
    section1 = r.Section(21324, "Proteomics", "This is a Proteomics example", "Not much", subsections=[subsection1_prot, subsection2_prot])
    section2 = r.Section(24324, "Transcriptomics", "This is a Transcriptomics example", "Not much", subsections=[subsection1_trans])
    
    # Add sections to the report
    report.sections.extend([section1, section2])
    
    # Create report view
    report_gui = r.StreamlitReportView(12312, "MyPage", report=report, columns=None)
    report_gui.generate_report(output_dir="tmp")
    report_gui.run_report(output_dir='tmp')