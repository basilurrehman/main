#!/usr/bin/env python3
"""
All Spec — info@ inbox cleanup (one-time backfill)
==================================================

Re-labels ~12k emails in info@allspecplumbing.com into 7 broad buckets and
archives the clutter. Built to be SAFE, STREAMING, and RESUMABLE.

Pipeline per thread:
    1. old-label map   -> if the thread already carries a known old label, use it
    2. deterministic   -> sender/subject rules
    3. Qwen (remote)    -> only the still-unresolved remainder (1-of-7, JSON out)
    4. low confidence   -> "Needs Review" (never guess)

SAFETY
    * DRY_RUN = True by default: writes CSV immediately, makes ZERO changes to Gmail.
    * Never deletes anything. Apply mode only ADDS labels + archives (removes INBOX).
    * Resumable: processed thread IDs are checkpointed to processed_threads.json.
"""

import os
import csv
import json
import time
import re
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------
DRY_RUN = True
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

# Remote API config from your curl
QWEN_BASE_URL = "http://148.230.96.46:8080"
QWEN_CHAT_PATH = "/api/chat"
QWEN_MODEL = "qwen3.5:2b"
API_USERNAME = "your_username"
API_PASSWORD = "clientwork"

# Batch size = number of threads per request
QWEN_BATCH = 3

# Parallel requests = how many 15-thread batches run simultaneously
# Set this to 2, 3, or 4.
QWEN_CONCURRENT_REQUESTS = 5

QWEN_CONFIDENCE_FLOOR = 0.70
QWEN_TIMEOUT = 300

DRYRUN_CSV = "cleanup_dryrun.csv"
CHECKPOINT = "processed_threads.json"
MANUAL_SKIP_THREADS = 0

BUCKETS = [
    "Lead",
    "Customer",
    "Suppliers & Contractors",
    "Finance",
    "For Nassim",
    "Promo",
    "Needs Review",
]

KEEP_IN_INBOX = {"Lead", "Customer", "Needs Review"}
CSV_FIELDS = ["thread_id", "sender", "subject", "bucket", "source", "confidence"]

# ----------------------------------------------------------------------------
# 1. OLD-LABEL -> NEW-BUCKET MAP
# ----------------------------------------------------------------------------
OLD_LABEL_MAP = {
    "New Enquiry form": "Lead", "Bider Installation Guys": "Lead",
    "Flat Rabe Now Quotes": "Lead", "SVC Quotes": "Lead", "Proud homes quote": "Lead",
    "Quotes": "Lead", "Proposals": "Lead", "New Build Plans": "Lead", "Artasker": "Lead",

    "2-Clients": "Customer", "Customer Corresponden...": "Customer", "Job": "Customer",
    "56 Caroline Dr": "Customer", "Fulton Hogan": "Customer", "Good Construction": "Customer",
    "TA Developments": "Customer", "R&S Body Corporate": "Customer",
    "CCTV Inspections": "Customer", "Roofing": "Customer", "book inspection": "Customer",
    "Barry Plant Noble Park": "Customer", "Bombay Realestate": "Customer",
    "First National": "Customer", "Ray White Epping": "Customer",
    "Timeless Real Estate": "Customer",

    "3 Suppliers": "Suppliers & Contractors", "Konnards": "Suppliers & Contractors",
    "Pro Plumbing": "Suppliers & Contractors", "Rnoce": "Suppliers & Contractors",
    "Swan Plumbing": "Suppliers & Contractors", "United Plumbing": "Suppliers & Contractors",
    "ACS Bathrooms": "Suppliers & Contractors", "AIF cloctrical": "Suppliers & Contractors",
    "Bomatrix": "Suppliers & Contractors", "Enviroinc": "Suppliers & Contractors",
    "Puretec": "Suppliers & Contractors", "Scoop Hire": "Suppliers & Contractors",
    "Stellar tiling & waterproofing": "Suppliers & Contractors",
    "Siris Design": "Suppliers & Contractors", "Muse Studios": "Suppliers & Contractors",
    "Pegasus Media": "Suppliers & Contractors", "Collings Media": "Suppliers & Contractors",
    "Marketing": "Suppliers & Contractors", "SEO Advantage": "Suppliers & Contractors",
    "PinPoint Local": "Suppliers & Contractors", "Webflow": "Suppliers & Contractors",

    "4- Finance": "Finance", "Accounting/Book Kooping": "Finance",
    "Accounts/Invoicing": "Finance", "Invoices": "Finance", "Statements": "Finance",
    "Remittance": "Finance", "Kennards Remittance": "Finance", "McCanns invoice": "Finance",
    "Mccans credit": "Finance", "Tradelink invoice": "Finance",
    "Drain solutions invoice": "Finance", "Afterpay": "Finance", "Humm": "Finance",
    "Pay.com": "Finance", "Paypal": "Finance", "American Express": "Finance",
    "CBA": "Finance", "CommBank": "Finance", "Fleet Card": "Finance", "Linkt": "Finance",
    "Vodafone": "Finance", "Insurances": "Finance", "WFI": "Finance",

    "Nassim Personal Emails": "For Nassim", "nassim to action": "For Nassim",

    "Coach HQ": "Promo", "Iman Gadzhi": "Promo", "Russell Brunson": "Promo",
    "Profitable Tradie": "Promo", "Mailchimp": "Promo", "Linkedin": "Promo",
    "Seek": "Promo", "Domain": "Promo", "Read Later": "Promo",

    "1-Action": "Needs Review", "Admin": "Needs Review", "Added to SME": "Needs Review",
    "AI APP": "Needs Review", "ENI": "Needs Review", "CatPis": "Needs Review",
    "Check & Inspect": "Needs Review", "End of day business sum...": "Needs Review",
    "ESV (Gas)": "Needs Review", "VBA": "Needs Review", "MEGT": "Needs Review",
    "Yarra Valley": "Needs Review", "Meetings": "Needs Review", "Office Shed": "Needs Review",
    "Old Emails": "Needs Review", "Service M8": "Needs Review",
    "VA's Archive/Actioned": "Needs Review", "AX3": "Needs Review", "39": "Needs Review",
}

# ----------------------------------------------------------------------------
# 2. DETERMINISTIC RULES
# ----------------------------------------------------------------------------
FINANCE_SENDERS = (
    "commbank", "cba", "americanexpress", "amex", "paypal", "afterpay",
    "humm", "vodafone", "linkt", "tradelink", "reece", "kennards", "wfi"
)
FINANCE_SUBJECT = re.compile(r"\b(invoice|receipt|statement|remittance|payment|bpay|overdue)\b", re.I)

PROMO_SENDERS = (
    "mailchimp", "linkedin", "seek", "domain.com", "imangadzhi",
    "russellbrunson", "profitabletradie", "coachhq"
)

LEAD_SUBJECT = re.compile(
    r"\b(quote|enquiry|inquiry|new lead|bidet|hot water|leak|blocked drain|gas|tap|toilet)\b",
    re.I,
)
LEAD_SENDERS = ("airtasker", "allspecleads")
NASSIM_HINTS = ("nassim",)


def deterministic_bucket(sender: str, subject: str) -> str | None:
    s = (sender or "").lower()
    subj = subject or ""
    if any(k in s for k in PROMO_SENDERS):
        return "Promo"
    if any(k in s for k in FINANCE_SENDERS) or FINANCE_SUBJECT.search(subj):
        return "Finance"
    if any(k in s for k in LEAD_SENDERS) or LEAD_SUBJECT.search(subj):
        return "Lead"
    if any(k in s for k in NASSIM_HINTS):
        return "For Nassim"
    return None


# ----------------------------------------------------------------------------
# 3. Remote classification
# ----------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You sort a plumbing company's emails into exactly one bucket. "
    "Buckets: Lead, Customer, Suppliers & Contractors, Finance, For Nassim, Promo, Needs Review. "
    "Return ONLY valid JSON. No explanation. No markdown. No code fences. "
    "Output format: "
    '[{"id":"<id>","label":"<bucket>","confidence":<0..1>}]'
)


def extract_response_text(data: dict) -> str:
    if isinstance(data, dict):
        if "choices" in data and data["choices"]:
            choice = data["choices"][0]
            if isinstance(choice, dict):
                msg = choice.get("message", {})
                if isinstance(msg, dict) and "content" in msg:
                    return msg.get("content") or ""
                if "text" in choice:
                    return choice.get("text") or ""
        if "message" in data and isinstance(data["message"], dict):
            return data["message"].get("content") or ""
        if "response" in data:
            return data.get("response") or ""
        if "content" in data:
            return data.get("content") or ""
    return ""


def extract_json_array(text: str) -> str:
    if not text:
        raise ValueError("Empty model response")
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON array found in model response")
    return text[start:end + 1]


def qwen_classify(batch, tag=""):
    """batch: list of dicts {id, sender, subject, snippet, email_count} -> list of {id,label,confidence}."""
    prefix = f"[{tag}] " if tag else ""
    print(f"\n=== {prefix}QWEN BATCH ({len(batch)} threads) ===")
    for b in batch:
        print(f"{b['id']} | {b['email_count']} emails | {b['sender']} | {b['subject'][:80]}")

    user = "Classify these emails:\n" + json.dumps([
        {
            "id": b["id"],
            "from": b["sender"],
            "subject": b["subject"],
            "snippet": b["snippet"][:200],
        }
        for b in batch
    ])

    print(f"{prefix}PROMPT CHARS: {len(user):,}")
    print(user[:1000])

    try:
        payload = {
            "model": QWEN_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "think": False,
            "options": {
                "think": False
            }
        }

        print(f"\n{prefix}PROMPT SENT TO REMOTE MODEL:")
        print(user[:2000])

        start = time.perf_counter()
        r = requests.post(
            f"{QWEN_BASE_URL}{QWEN_CHAT_PATH}",
            json=payload,
            auth=(API_USERNAME, API_PASSWORD),
            timeout=QWEN_TIMEOUT,
        )
        r.raise_for_status()

        elapsed = time.perf_counter() - start
        data = r.json()
        text = extract_response_text(data)

        print(f"{prefix}REMOTE MODEL TIME: {elapsed:.2f}s ({len(batch)} threads)")
        print(f"\n{prefix}MODEL RESPONSE:")
        print(text[:3000])

        json_text = extract_json_array(text)
        out = {o["id"]: o for o in json.loads(json_text)}

    except Exception as e:
        print(f"{prefix}! Remote batch failed ({e}); routing batch to Needs Review")
        out = {}

    results = []
    for b in batch:
        o = out.get(b["id"])
        if (
            not o
            or o.get("label") not in BUCKETS
            or float(o.get("confidence", 0)) < QWEN_CONFIDENCE_FLOOR
        ):
            result = {"id": b["id"], "label": "Needs Review", "confidence": 0.0}
        else:
            result = {"id": b["id"], "label": o["label"], "confidence": float(o["confidence"])}

        results.append(result)
        print(f"{prefix}QWEN RESULT -> {b['id']} => {result['label']} ({result['confidence']})")

    return results


def chunked(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def flush_pending_for_qwen(
    pending_for_qwen,
    rows,
    csv_writer,
    csv_file,
    done,
    seen,
    counts,
    total_threads_seen,
    total_emails_seen,
):
    """
    Sends as many 15-thread batches as possible, up to QWEN_CONCURRENT_REQUESTS running simultaneously.
    This is where the parallelism happens.
    """
    if not pending_for_qwen:
        return seen, counts

    batches = list(chunked(pending_for_qwen, QWEN_BATCH))
    pending_for_qwen.clear()

    max_workers = max(1, min(QWEN_CONCURRENT_REQUESTS, len(batches)))
    print(f"\nDISPATCHING {len(batches)} QWEN BATCH(ES) WITH {max_workers} PARALLEL REQUEST(S)")
    
    wave_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_meta = {}
        for i, batch in enumerate(batches, start=1):
            future = executor.submit(qwen_classify, batch, f"REQ-{i}")
            future_to_meta[future] = (i, batch)

        for future in as_completed(future_to_meta):
            req_no, batch = future_to_meta[future]
            try:
                qwen_batches = future.result()
            except Exception as e:
                print(f"[REQ-{req_no}] unexpected failure ({e}); routing whole batch to Needs Review")
                qwen_batches = [{"id": src["id"], "label": "Needs Review", "confidence": 0.0} for src in batch]

            src_map = {b["id"]: b for b in batch}

            for res in qwen_batches:
                src = src_map[res["id"]]
                row = {
                    "thread_id": res["id"],
                    "sender": src["sender"],
                    "subject": src["subject"],
                    "bucket": res["label"],
                    "source": "qwen",
                    "confidence": res["confidence"],
                }

                rows.append(row)
                csv_writer.writerow(row)
                csv_file.flush()

                done.add(res["id"])
                save_checkpoint(done)
                seen += 1
                counts[row["bucket"]] = counts.get(row["bucket"], 0) + 1
                print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done)
        wave_elapsed = time.perf_counter() - wave_start

        print(
            f"\n============== WAVE COMPLETE =========== | "
            f"\n====================================== | "
            f"\n============== ========== =========== | "
            f"\n============== =========== =========== | "
            f"\n============== ========= =========== | "
            f"BATCHES={len(batches)} | "
            f"TIME={wave_elapsed:.2f}s"
        )
    return seen, counts


# ----------------------------------------------------------------------------
# Gmail helpers
# ----------------------------------------------------------------------------
def gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def load_checkpoint():
    if not os.path.exists(CHECKPOINT):
        return set()
    try:
        with open(CHECKPOINT, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_checkpoint(done):
    tmp = CHECKPOINT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(sorted(done), f)
    os.replace(tmp, CHECKPOINT)


def header(msg, name):
    for h in msg.get("payload", {}).get("headers", []):
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done):
    print(
        f"PROCESSED={seen} | "
        f"SEEN={total_threads_seen} | "
        f"PENDING_QWEN={len(pending_for_qwen)} | "
        f"CHECKPOINTED={len(done)} | "
        f"EMAILS_SEEN={total_emails_seen}"
    )


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    svc = gmail_service()

    labels = svc.users().labels().list(userId="me").execute().get("labels", [])
    id2name = {l["id"]: l["name"] for l in labels}
    name2id = {l["name"]: l["id"] for l in labels}

    if not DRY_RUN:
        for b in BUCKETS:
            if b not in name2id:
                created = svc.users().labels().create(
                    userId="me",
                    body={
                        "name": b,
                        "labelListVisibility": "labelShow",
                        "messageListVisibility": "show",
                    },
                ).execute()
                name2id[b] = created["id"]

    done = load_checkpoint()
    save_checkpoint(done)

    print("CHECKPOINT PATH:", os.path.abspath(CHECKPOINT))
    print("CSV PATH:", os.path.abspath(DRYRUN_CSV))

    print("Counting threads...")
    total_threads = 0
    page_token = None

    while True:
        r = svc.users().threads().list(
            userId="me",
            maxResults=500,
            pageToken=page_token,
        ).execute()

        total_threads += len(r.get("threads", []))
        page_token = r.get("nextPageToken")
        if not page_token:
            break

    print(f"TOTAL THREADS FOUND: {total_threads}")
    print(f"ALREADY PROCESSED: {len(done)}")
    print(f"REMAINING: {total_threads - len(done)}")

    rows = []
    pending_for_qwen = []
    page = None

    seen = 0
    total_threads_seen = 0
    total_emails_seen = 0
    skipped_checkpoint = 0
    skipped_manual = 0

    csv_exists = os.path.exists(DRYRUN_CSV)
    csv_file = open(DRYRUN_CSV, "a", newline="", encoding="utf-8")
    csv_writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)

    if (not csv_exists) or os.path.getsize(DRYRUN_CSV) == 0:
        csv_writer.writeheader()
        csv_file.flush()

    counts = {b: 0 for b in BUCKETS}

    try:
        while True:
            resp = svc.users().threads().list(
                userId="me",
                maxResults=100,
                pageToken=page,
            ).execute()

            thread_list = resp.get("threads", [])
            print(f"\nPAGE THREADS: {len(thread_list)}")

            for t in thread_list:
                total_threads_seen += 1
                tid = t["id"]

                if total_threads_seen <= MANUAL_SKIP_THREADS:
                    skipped_manual += 1
                    print(f"SKIP MANUAL #{total_threads_seen}: {tid}")
                    continue

                if tid in done:
                    skipped_checkpoint += 1
                    print(f"SKIP CHECKPOINTED #{total_threads_seen}: {tid}")
                    continue

                print(f"\nTHREAD #{total_threads_seen}")
                print(f"THREAD: {tid}")

                thread = svc.users().threads().get(
                    userId="me",
                    id=tid,
                    format="metadata",
                    metadataHeaders=["From", "Subject"],
                ).execute()

                msgs = thread.get("messages", [])
                email_count = len(msgs)
                print(f"EMAILS IN THREAD: {email_count}")

                if not msgs:
                    row = {
                        "thread_id": tid,
                        "sender": "",
                        "subject": "",
                        "bucket": "Needs Review",
                        "source": "empty-thread",
                        "confidence": 0.0,
                    }
                    rows.append(row)
                    csv_writer.writerow(row)
                    csv_file.flush()
                    done.add(tid)
                    save_checkpoint(done)
                    seen += 1
                    counts[row["bucket"]] += 1
                    print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done)
                    continue

                total_emails_seen += email_count

                first = msgs[0]
                sender = header(first, "From")
                subject = header(first, "Subject")
                print(f"FROM: {sender}")
                print(f"SUBJECT: {subject}")

                thread_snippet = (thread.get("snippet") or " ".join(m.get("snippet", "") for m in msgs))[:250]

                cur_label_names = {id2name.get(lid) for m in msgs for lid in m.get("labelIds", [])}
                cur_label_names = {x for x in cur_label_names if x}
                print(f"OLD LABELS: {sorted(cur_label_names)}")

                mapped = {OLD_LABEL_MAP[n] for n in cur_label_names if n in OLD_LABEL_MAP}
                print(f"MAPPED BUCKETS: {mapped}")

                if len(mapped) == 1:
                    bucket = next(iter(mapped))
                    source = "old-label"
                    print(f"CLASSIFIED BY OLD LABEL -> {bucket}")

                    row = {
                        "thread_id": tid,
                        "sender": sender,
                        "subject": subject,
                        "bucket": bucket,
                        "source": source,
                        "confidence": 1.0,
                    }

                    rows.append(row)
                    csv_writer.writerow(row)
                    csv_file.flush()
                    done.add(tid)
                    save_checkpoint(done)
                    seen += 1
                    counts[bucket] += 1
                    print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done)
                    continue

                if len(mapped) > 1:
                    bucket = "Needs Review"
                    source = "old-label-conflict"
                    print("CLASSIFIED BY OLD LABEL -> Needs Review (conflict)")

                    row = {
                        "thread_id": tid,
                        "sender": sender,
                        "subject": subject,
                        "bucket": bucket,
                        "source": source,
                        "confidence": 1.0,
                    }

                    rows.append(row)
                    csv_writer.writerow(row)
                    csv_file.flush()
                    done.add(tid)
                    save_checkpoint(done)
                    seen += 1
                    counts[bucket] += 1
                    print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done)
                    continue

                bucket = deterministic_bucket(sender, subject)
                if bucket:
                    source = "rule"
                    print(f"CLASSIFIED BY RULE -> {bucket}")

                    row = {
                        "thread_id": tid,
                        "sender": sender,
                        "subject": subject,
                        "bucket": bucket,
                        "source": source,
                        "confidence": 1.0,
                    }

                    rows.append(row)
                    csv_writer.writerow(row)
                    csv_file.flush()
                    done.add(tid)
                    save_checkpoint(done)
                    seen += 1
                    counts[bucket] += 1
                    print_progress(seen, total_threads_seen, total_emails_seen, pending_for_qwen, done)
                else:
                    pending_for_qwen.append(
                        {
                            "id": tid,
                            "sender": sender,
                            "subject": subject,
                            "snippet": thread_snippet,
                            "email_count": email_count,
                        }
                    )
                    print("SENDING TO QWEN")

            # As soon as we have enough unresolved threads, send them in parallel batches.
            if len(pending_for_qwen) >= QWEN_BATCH:
                seen, counts = flush_pending_for_qwen(
                    pending_for_qwen,
                    rows,
                    csv_writer,
                    csv_file,
                    done,
                    seen,
                    counts,
                    total_threads_seen,
                    total_emails_seen,
                )

            page = resp.get("nextPageToken")
            print(f"processed ~{seen} threads...")
            if not page:
                break

        # Final flush for leftovers, including smaller-than-15 tail batches.
        while pending_for_qwen:
            seen, counts = flush_pending_for_qwen(
                pending_for_qwen,
                rows,
                csv_writer,
                csv_file,
                done,
                seen,
                counts,
                total_threads_seen,
                total_emails_seen,
            )

        print("\nDONE")
        print(f"THREADS FOUND: {total_threads}")
        print(f"THREADS SEEN THIS RUN: {total_threads_seen}")
        print(f"THREADS PROCESSED THIS RUN: {seen}")
        print(f"EMAILS SEEN THIS RUN: {total_emails_seen}")
        print(f"SKIPPED CHECKPOINT: {skipped_checkpoint}")
        print(f"SKIPPED MANUAL: {skipped_manual}")
        print("Distribution:", json.dumps(counts, indent=2))

        if DRY_RUN:
            print(f"\nDRY RUN complete -> {DRYRUN_CSV}")
            print("No changes made to Gmail.")
        else:
            for r in rows:
                add = [name2id[r["bucket"]]]
                remove = [] if r["bucket"] in KEEP_IN_INBOX else ["INBOX"]
                svc.users().threads().modify(
                    userId="me",
                    id=r["thread_id"],
                    body={"addLabelIds": add, "removeLabelIds": remove},
                ).execute()
                time.sleep(0.02)

            print(f"APPLIED labels to {len(rows)} threads. Old labels left intact for now.")

    finally:
        try:
            csv_file.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()