def test_imports():
    import vuegen
    import vuegen.__main__
    import vuegen.plot_utils
    import vuegen.quarto_reportview
    import vuegen.report
    import vuegen.report_generator
    import vuegen.streamlit_reportview
    import vuegen.utils

    assert vuegen.__version__
