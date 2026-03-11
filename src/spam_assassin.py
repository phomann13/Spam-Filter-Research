# ── Download & parse all SpamAssassin public corpus files ─────────
import os
import tarfile
import urllib.request
import email
from email import policy
from email.parser import BytesParser
from io import BytesIO
import pandas as pd

BASE_URL = "https://spamassassin.apache.org/old/publiccorpus/"

# All files with their labels — hard_ham is still ham
FILES = {
    "20021010_easy_ham.tar.bz2"  : "ham",
    "20021010_hard_ham.tar.bz2"  : "ham",
    "20021010_spam.tar.bz2"      : "spam",
    "20030228_easy_ham.tar.bz2"  : "ham",
    "20030228_easy_ham_2.tar.bz2": "ham",
    "20030228_hard_ham.tar.bz2"  : "ham",
    "20030228_spam.tar.bz2"      : "spam",
    "20030228_spam_2.tar.bz2"    : "spam",
    "20050311_spam_2.tar.bz2"    : "spam",
}

DOWNLOAD_DIR = "spamassassin_raw"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ── Step 1: Download ──────────────────────────────────────────────
for filename in FILES:
    dest = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(dest):
        print(f"[SKIP] {filename} already downloaded")
        continue
    url = BASE_URL + filename
    print(f"[DOWNLOAD] {filename} ...")
    urllib.request.urlretrieve(url, dest)
    print(f"  -> saved to {dest}")

# ── Step 2: Parse each email file ────────────────────────────────
def parse_email_bytes(raw_bytes):
    """Extract subject + body from raw email bytes."""
    try:
        msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)
        subject = str(msg.get("subject", "") or "")
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_content()
                        break
                    except Exception:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode("utf-8", errors="ignore")
                            break
        else:
            try:
                body = msg.get_content()
            except Exception:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode("utf-8", errors="ignore")

        return subject.strip(), body.strip()
    except Exception as e:
        return "", ""

rows = []

for filename, label in FILES.items():
    tar_path = os.path.join(DOWNLOAD_DIR, filename)
    # Extract date prefix from filename for tracking
    date_prefix = filename.split("_")[0]  # e.g. "20021010"
    
    print(f"[PARSE] {filename} ({label}) ...")
    
    with tarfile.open(tar_path, "r:bz2") as tar:
        for member in tar.getmembers():
            # Skip directories and cmds file (non-email metadata file)
            if member.isdir():
                continue
            if os.path.basename(member.name) == "cmds":
                continue
            
            try:
                f = tar.extractfile(member)
                if f is None:
                    continue
                raw_bytes = f.read()
                subject, body = parse_email_bytes(raw_bytes)
                
                if not body and not subject:
                    continue
                    
                rows.append({
                    "subject"     : subject,
                    "body"        : body,
                    "message"     : (subject + " " + body).strip(),
                    "label"       : 1 if label == "spam" else 0,
                    "spam_ham"    : label,
                    "source_file" : filename,
                    "date_batch"  : date_prefix,
                })
            except Exception as e:
                continue

# ── Step 3: Build DataFrame ───────────────────────────────────────
sa_df = pd.DataFrame(rows)

print(f"\n=== SpamAssassin Corpus Summary ===")
print(f"Total emails : {len(sa_df):,}")
print(f"Ham          : {(sa_df['label']==0).sum():,} ({(sa_df['label']==0).mean()*100:.1f}%)")
print(f"Spam         : {(sa_df['label']==1).sum():,} ({(sa_df['label']==1).mean()*100:.1f}%)")
print(f"\nBy source file:")
print(sa_df.groupby(['source_file','spam_ham'])['label']
          .count().rename("count").to_string())

# ── Step 4: Save ──────────────────────────────────────────────────
sa_df.to_csv("spamassassin_corpus.csv", index=False)
print(f"\nSaved to spamassassin_corpus.csv")
sa_df.head(3)