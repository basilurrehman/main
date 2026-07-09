import re
import json
import argparse
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except Exception:
    BeautifulSoup = None

LABELS = [
    "Title",
    "Agency",
    "State",
    "NAICS Code",
    "Industry",
    "Solicitation Type",
    "Solicitation ID",
    "Open Date",
    "Pre-Bid Meeting Date",
    "Questions Due Date",
    "Close Date",
    "Project Duration",
    "Last Updated",
    "Description",
    "Attached Files",
    "Contact Information",
    "Budget Estimate (AI)"
]


def extract_text_from_html(html_text):
    if BeautifulSoup:
        soup = BeautifulSoup(html_text, "html.parser")
        # get visible text with sensible separators
        text = soup.get_text("\n")
    else:
        # fallback: very naive tag stripper
        text = re.sub(r"<script[\s\S]*?<\/script>", "", html_text, flags=re.I)
        text = re.sub(r"<style[\s\S]*?<\/style>", "", text, flags=re.I)
        text = re.sub(r"<[^>]+>", "\n", text)
    # normalize whitespace
    text = re.sub(r"\r\n|\r", "\n", text)
    text = re.sub(r"\t", " ", text)
    return text


def is_label_line(line_lower):
    for lab in LABELS:
        if lab.lower() + ":" in line_lower:
            return True
    return False


def parse_text_blocks(text):
    lines = [l.strip() for l in text.splitlines()]
    # find line indices for labels
    indices = {}
    for i, line in enumerate(lines):
        low = line.lower()
        for lab in LABELS:
            key = lab.lower()
            if key + ":" in low and key not in indices:
                indices[key] = i
    # build results
    results = {}
    for idx, lab in enumerate(LABELS):
        key = lab.lower()
        if key not in indices:
            results[key] = ""
            continue
        start = indices[key]
        line = lines[start]
        # content after colon on same line
        if ":" in line:
            after = line.split(":", 1)[1].strip()
        else:
            after = ""
        # gather subsequent lines until next label
        content_lines = [after] if after else []
        # determine next label line index
        next_idxs = [v for k, v in indices.items() if v > start]
        end = min(next_idxs) if next_idxs else len(lines)
        for j in range(start + 1, end):
            # stop if this line is another label
            lowj = lines[j].lower()
            if is_label_line(lowj):
                break
            content_lines.append(lines[j])
        # join and normalize
        value = "\n".join([c for c in content_lines if c])
        results[key] = value.strip()
    return results


def post_process(results):
    # try to extract structured contact info
    contact = results.get("contact information", "")
    contact_dict = {}
    if contact:
        # email
        m = re.search(r"([\w\.-]+@[\w\.-]+)", contact)
        if m:
            contact_dict["email"] = m.group(1)
        # phone
        m = re.search(r"(\(\d{3}\)\s*\d{3}[-\s]\d{4}|\d{3}[-\s]\d{3}[-\s]\d{4})", contact)
        if m:
            contact_dict["phone"] = m.group(1)
        # name (first non-empty line)
        for line in contact.splitlines():
            line = line.strip()
            if line and not re.search(r"@|\d{3}[-\s]\d{3}", line):
                contact_dict.setdefault("name", line)
                break
    if contact_dict:
        results["contact information"] = contact_dict
    # find any URLs in the whole text fallback
    all_text = "\n".join([v if isinstance(v, str) else json.dumps(v) for v in results.values()])
    pattern = r'https?://[^\s\'\"]+'
    urls = re.findall(pattern, all_text)
    if urls:
        results["link_to_bid_source"] = urls[0]
    # split budget estimate (AI) into numeric range and descriptive text
    budget_key = "budget estimate (ai)"
    if budget_key in results and results[budget_key]:
        raw = results[budget_key]
        # try to find a numeric range like "$24,000,000 – $32,000,000" or with hyphen/to
        range_match = re.search(r"\$?[\d,]+(?:\.\d+)?\s*(?:–|—|-|to)\s*\$?[\d,]+(?:\.\d+)?", raw)
        if range_match:
            amount_text = range_match.group(0)
            nums = re.findall(r"\$?([\d,]+(?:\.\d+)?)", amount_text)
            results["budget_estimate_ai_amount"] = amount_text
            if len(nums) >= 2:
                results["budget_estimate_ai_min"] = nums[0]
                results["budget_estimate_ai_max"] = nums[1]
            # remove the matched amount from the raw note
            note = (raw[:range_match.start()] + raw[range_match.end():]).strip()
        else:
            results["budget_estimate_ai_amount"] = ""
            note = raw.strip()
        # store the remaining descriptive text
        results["budget_estimate_ai_note"] = note

        # extract site visit and mandatory flag from pre-bid meeting date
        pb_key = "pre-bid meeting date"
        if pb_key in results and results[pb_key]:
            raw_pb = results[pb_key]
            # mandatory flag
            results["pre bid meeting mandatory"] = bool(re.search(r"\bmandatory\b", raw_pb, re.I))
            # primary date (first date found)
            m = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", raw_pb)
            if m:
                results[pb_key] = m.group(1)
            else:
                results[pb_key] = raw_pb.strip()
            # site visit date (try explicit label, else second date)
            m2 = re.search(r"site visit date[:\s]*([\d/\-]+)", raw_pb, re.I)
            if m2:
                results["site visit date"] = m2.group(1)
            else:
                dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", raw_pb)
                if len(dates) >= 2:
                    results["site visit date"] = dates[1]

        # extract projected award date from close date field
        cd_key = "close date"
        if cd_key in results and results[cd_key]:
            raw_cd = results[cd_key]
            m = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", raw_cd)
            if m:
                results[cd_key] = m.group(1)
            else:
                results[cd_key] = raw_cd.strip()
            m2 = re.search(r"projected award date[:\s]*([\d/\-]+)", raw_cd, re.I)
            if m2:
                results["projected award date"] = m2.group(1)
            else:
                dates = re.findall(r"(\d{1,2}/\d{1,2}/\d{4})", raw_cd)
                if len(dates) >= 2:
                    results["projected award date"] = dates[1]
    # normalize keys: replace spaces with underscores for JSON keys
    normalized = {}
    for k, v in results.items():
        newk = k.replace(" ", "_").lower()
        normalized[newk] = v
    return normalized


def main():
    p = argparse.ArgumentParser(description="Parse bid HTML and output JSON with fields.")
    p.add_argument("html_file", help="Path to input HTML file")
    p.add_argument("-o", "--output", default="parsed_bid.json", help="Output JSON file path")
    args = p.parse_args()

    path = Path(args.html_file)
    if not path.exists():
        print(f"Input file not found: {path}")
        return
    html = path.read_text(encoding="utf-8", errors="ignore")
    text = extract_text_from_html(html)
    blocks = parse_text_blocks(text)
    result = post_process(blocks)

    out_path = Path(args.output)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote JSON to {out_path}")


if __name__ == "__main__":
    main()
