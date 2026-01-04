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

See [RUNNING.md](RUNNING.md) for detailed local setup instructions.
