import json
import psycopg2
from pathlib import Path

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "irtm_db",
    "user": "irtm_user",
    "password": "irtm_pass"
}

JSON_PATH = r"3_Al_Quran_Dataset_FINAL.json"

def normalize_simple(text):
    if text is None:
        return None
    return text.strip()

def batch_insert_quran(records):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    sql = """
    INSERT INTO quran_ayah
    (quran_id, juz_id, surah_id, ayah_id, source,
     transliteration, surah_name_ar, surah_name_ur, surah_name_en, surah_type,
     text_ar, text_ur, text_en)
    VALUES
    (%s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s,
     %s, %s, %s)
    ON CONFLICT (quran_id) DO NOTHING;
    """

    batch = []
    for r in records:
        batch.append((
            r.get("quran_id"),
            r.get("juz"),
            r.get("surah_id"),
            r.get("ayah_id"),
            r.get("source", "Quran"),
            normalize_simple(r.get("transliteration")),
            normalize_simple(r.get("surah_name_ar")),
            normalize_simple(r.get("surah_name_ur")),
            normalize_simple(r.get("surah_name_en")),
            normalize_simple(r.get("surah_type")),
            r.get("text_ar"),
            r.get("text_ur"),
            r.get("text_en")
        ))

    cur.executemany(sql, batch)
    conn.commit()
    conn.close()

    print(f"Inserted {len(batch)} rows.")

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    batch_insert_quran(data)

if __name__ == "__main__":
    main()
