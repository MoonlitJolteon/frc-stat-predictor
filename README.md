## Installation and Setup

1.  **Prerequisites:**
    *   Python 3.8+
    *   [Ollama](https://ollama.com/)

2.  **Clone the Repository:** (If you have not already, skip if you have the file contents)

3.  **Create a Virtual Environment:**

    ```
    python -m venv .venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

4.  **Install Dependencies:**

    ```
    pip install -r requirements.txt
    ```

5.  **Set up Ollama:**

    *   Download and install Ollama from [https://ollama.com/](https://ollama.com/).
    *   Run `ollama pull <model_name>` to download the desired language model (e.g., `ollama pull llama2`).

## Configuration

1.  **Configure:**
    *   The code uses `config.json.example` as a template. Copy this file to `config.json`.
    *   Edit `config.json` to provide 
        *   The Blue Alliance (TBA) API key
        *   Indiana Scouting Alliance (ISA) API key
        *   Preferred Ollama model


## Running the Application

1.  **Run the Main Script:**

    ```
    python main.py
    ```
2.  [**Open the page in your browser**](http://localhost:5000)