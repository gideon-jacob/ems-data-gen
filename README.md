# EMS Data Generator

This project generates simulated environmental sensor data and uploads it to Supabase.

## Components

-   `data_gen.py`: Generates sensor data and appends it to `data.csv`.
-   `cloud_worker.py`: Reads entries from `data.csv`, uploads them to a Supabase table (`readings`), and clears the file.

## Setup & Running

### Option 1: Docker (Recommended)

1.  Ensure you have Docker and Docker Compose installed.
2.  Create a `.env` file with your Supabase credentials:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```
3.  Run the application:
    ```bash
    docker-compose up --build
    ```

### Option 2: Local Python

1.  **Create a Virtual Environment**
    Open your terminal/command prompt in the project directory (`ems-data-gen`) and run:
    ```powershell
    python -m venv venv
    ```

2.  **Activate the Virtual Environment**
    *   **Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate
        ```
    *   **Windows (Command Prompt):**
        ```cmd
        venv\Scripts\activate.bat
        ```
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    With the virtual environment activated, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables**
    Ensure you have a `.env` file in the project root with your Supabase credentials:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    ```

### Execution

You will need to run two scripts in parallel (open two terminal windows).

**Terminal 1: Data Generator**
This script generates sensor data and writes it to `data.csv`.
```bash
python src/data_gen.py
```

**Terminal 2: Cloud Worker**
This script reads `data.csv`, sends the data to Supabase, and clears the file.
```bash
python src/cloud_worker.py
```

 