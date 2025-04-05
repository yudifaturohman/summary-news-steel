# Summary News Steel

Summary News Steel is a Python-based project that aims to automatically retrieve the latest news about the steel industry from various sources, then generate news summaries using AI to facilitate understanding and distribution of important information.

## Main Feature

- Automated Web Scraping: Retrieves the latest news from trusted websites in the steel industry.
- AI Summary Generator: Uses AI technology to summarize news content accurately and concisely.
- Structured Storage: Stores scraping and summary results into a database for better management.
- Scheduled Automation: Support for scheduling scraping and summary on a regular basis (using cron job or task scheduler).
- Map Reduce Chain: The Map Reduce Chain approach is a pragmatic solution for summarization. It's a two-step process that simplifies the task of summarizing a document.
  
  ![Unknown](https://github.com/user-attachments/assets/ef638ab2-849e-42da-a9da-a5260e8421f4)
  ![Unknown-2](https://github.com/user-attachments/assets/47eef3f0-72f3-4bd6-9878-8d4313e4955d)

  

## Tech Stack

- Python
- Beutifulshop
- LangChain
- Postgree SQL
- Groq Cloud
- Llama3.1

## Requirements

- Python 3.7 or higher
- The following Python packages (listed in `requirements.txt`)

## Setup

1. Clone the repository and navigate to the project directory.
   ```sh
   git clone https://github.com/yudifaturohman/summary-news-steel.git
   cd summary-news-steel
   ```
2. Create environment project.
   ```sh
   python -m venv venv
   ```
3. Activate environment.
   - MacOS
   ```sh
   source venv/bin/activate
   ```
   - Windows
   ```sh
   venv\Scripts\activate.bat
   ```
   or
   
   ```sh
   venv\Scripts\Activate.ps1
   ```
4. Install the required packages using pip:
   ```sh
   pip install -r requirements.txt
   ```
5. Set the environment variable with your project. You can do this by creating a `.env` file in the project directory with the following content:
   ```
    DB_NAME=your_database
    DB_USER=username
    DB_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
    GROQ_API_KEY=your_groq_api_key

    EMAIL_SENDER=your_sender_email
    EMAIL_PASSWORD=your_app_password
    EMAIL_RECEIVER=receiver_email
   ```

## Running the Application

1. To run Summary News, use the following command:

```sh
python summary_news.py
```

2. Running scrape script

```sh
python scraping_news.py
```
> Can you running automatic with Cron Jobs (Linux) or Task Schedular (Windows)
