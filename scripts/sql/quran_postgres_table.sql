-- 1) Main canonical table
CREATE TABLE IF NOT EXISTS quran_ayah (
    quran_id        INT PRIMARY KEY,
    juz_id          INT,
    surah_id        INT,
    ayah_id         INT,
    source          VARCHAR(50) DEFAULT 'Quran',
    transliteration VARCHAR(200),
    surah_name_ar   VARCHAR(200),
    surah_name_ur   VARCHAR(200),
    surah_name_en   VARCHAR(200),
    surah_type      VARCHAR(50),
    text_ar         TEXT,
    text_ur         TEXT,
    text_en         TEXT
);

-- 2) Indexes for fast filters
CREATE INDEX IF NOT EXISTS idx_quran_surah_id ON quran_ayah (surah_id);
CREATE INDEX IF NOT EXISTS idx_quran_juz_id   ON quran_ayah (juz_id);
CREATE INDEX IF NOT EXISTS idx_quran_ayah_id  ON quran_ayah (ayah_id);
CREATE INDEX IF NOT EXISTS idx_quran_source   ON quran_ayah (source);
