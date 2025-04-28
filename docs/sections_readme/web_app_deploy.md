## Web application deployment

Once a Streamlit report is generated, it can be deployed as a web application to make it accessible online. There are multiple ways to achieve this:

- **Streamlit Community Cloud**: Deploy your report easily using [Streamlit Cloud](https://streamlit.io/cloud), as demonstrated in the [EMP VueGen Demo](https://earth-microbiome-vuegen-demo.streamlit.app/). The process involves moving the necessary scripts, data, and a requirements.txt file into a GitHub repository. Then, the app can be deployed via the Streamlit Cloud interface. The deployment example is available in the `streamlit-report-example` branch.
- **Standalone Executables**: Convert your Streamlit application into a desktop app by packaging it as an executable file for different operating systems. A detailed explanation of this process can be found in this [Streamlit forum post](https://discuss.streamlit.io/t/streamlit-deployment-as-an-executable-file-exe-for-windows-macos-and-android/6812).
- **Stlite**: Run Streamlit apps directly in the browser with (https://github.com/whitphx/stlite)(https://github.com/whitphx/stlite), a WebAssembly port of Streamlit powered by Pyodide, eliminating the need for a server. It also allows packaging apps as standalone desktop executables using stlite desktop.

These options provide flexibility depending on whether the goal is online accessibility, lightweight execution, or local application distribution.