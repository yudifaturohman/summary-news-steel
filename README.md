# Summary News Steel

Summary News Steel adalah proyek berbasis Python yang bertujuan untuk mengambil berita-berita terbaru seputar industri baja (steel) dari berbagai sumber secara otomatis, lalu menghasilkan ringkasan berita menggunakan AI untuk mempermudah pemahaman dan distribusi informasi penting.

## Fitur Utama

- Web Scraping Otomatis: Mengambil berita terbaru dari situs-situs terpercaya di bidang industri baja.
- AI Summary Generator: Menggunakan teknologi AI untuk meringkas konten berita secara akurat dan ringkas.
- Penyimpanan Terstruktur: Menyimpan hasil scraping dan ringkasan ke dalam database untuk pengelolaan yang lebih baik.
- Scheduled Automation: Dukungan untuk penjadwalan scraping dan summary secara berkala (menggunakan cron job atau task scheduler).

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