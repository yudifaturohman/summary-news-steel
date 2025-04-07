import os
import time
import textwrap
import smtplib
import markdown
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain, ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq

# === Load ENV ===
load_dotenv()

# === LLM SETUP ===
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=512,
    api_key=os.getenv("GROQ_API_KEY")
)

# === DB SETUP ===
def init_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            filename TEXT PRIMARY KEY,
            summary TEXT,
            is_sent BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    return conn

def is_already_summarized(conn, filename):
    c = conn.cursor()
    c.execute("SELECT 1 FROM summaries WHERE filename = %s", (filename,))
    return c.fetchone() is not None

def save_summary_to_db(conn, filename, summary):
    c = conn.cursor()
    c.execute("""
        INSERT INTO summaries (filename, summary)
        VALUES (%s, %s)
        ON CONFLICT (filename) DO UPDATE SET summary = EXCLUDED.summary
    """, (filename, summary))
    conn.commit()

# === TEXT SPLITTER ===
def split_docs(documents, chunk_size=500, chunk_overlap=20):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "\n\n\n", " ", ""],
    )
    return splitter.split_documents(documents)

# === SUMMARIZATION CHAIN ===
map_prompt = PromptTemplate.from_template("""Write a concise summary of the following content:\n\n{text}\n\nSummary:""")
reduce_prompt = PromptTemplate.from_template("""The Following is set of summaries:\n\n{doc_summaries}\n\nSummarize the above summaries with all the key details\n\nSummary:""")

map_chain = LLMChain(prompt=map_prompt, llm=llm)
reduce_chain_llm = LLMChain(llm=llm, prompt=reduce_prompt)
stuff_chain = StuffDocumentsChain(llm_chain=reduce_chain_llm, document_variable_name="doc_summaries")
reduce_chain = ReduceDocumentsChain(combine_documents_chain=stuff_chain)

map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    document_variable_name="text",
    reduce_documents_chain=reduce_chain
)

# === EMAIL ===
def send_email(subject, body, to_email, from_email, from_password):
    body_html = markdown.markdown(body)

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, from_password)
        server.send_message(msg)

def send_unsent_summaries(conn, to_email, from_email, from_password):
    c = conn.cursor()
    c.execute("SELECT filename, summary FROM summaries WHERE is_sent = FALSE")
    rows = c.fetchall()

    if not rows:
        print("📭 Tidak ada ringkasan yang perlu dikirim.")
        return

    for filename, summary in rows:
        try:
            subject = f"Ringkasan Berita: {filename}"
            send_email(subject, summary, to_email, from_email, from_password)
            print(f"📨 Email terkirim untuk: {filename}")

            c.execute("UPDATE summaries SET is_sent = TRUE WHERE filename = %s", (filename,))
            conn.commit()
        except Exception as e:
            print(f"❌ Gagal kirim email untuk {filename}: {e}")

# === WATCHDOG HANDLER ===
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, conn, folder_path):
        self.conn = conn
        self.folder_path = folder_path

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".txt"):
            return

        time.sleep(1)  # delay sebentar biar file selesai disalin
        filename = os.path.basename(event.src_path)

        if is_already_summarized(self.conn, filename):
            print(f"✅ Sudah diringkas sebelumnya: {filename}")
            return

        print(f"📥 File baru terdeteksi: {filename}")
        loader = TextLoader(event.src_path, autodetect_encoding=True)
        documents = loader.load()
        docs = split_docs(documents)

        print(f"🧠 Merangkum {filename}...")
        summary = map_reduce_chain.run(docs)
        save_summary_to_db(self.conn, filename, summary)

        print(f"✅ Summary selesai: {filename}")
        send_unsent_summaries(
            self.conn,
            to_email=os.getenv("EMAIL_RECEIVER"),
            from_email=os.getenv("EMAIL_SENDER"),
            from_password=os.getenv("EMAIL_PASSWORD")
        )

# === MAIN ===
def main():
    folder_path = "News"
    conn = init_db()

    event_handler = NewFileHandler(conn, folder_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print("👀 Menunggu file baru di folder 'News/'...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Dihentikan oleh pengguna.")
    observer.join()
    conn.close()

if __name__ == "__main__":
    main()
