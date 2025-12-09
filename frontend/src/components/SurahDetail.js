import React from 'react';
import QuranData from '../dataset/AL_Quran_Dataset.json';
import './SurahDetail.css';

const SurahDetail = ({ surahId, onBack }) => {
  if (!surahId) return null;

  const ayahs = QuranData
    .filter(item => item.surah_id === surahId)
    .sort((a, b) => (a.ayah_id || 0) - (b.ayah_id || 0));

  const surahName = ayahs.length ? ayahs[0].surah_name_ar || ayahs[0].surah_name_en : `سورہ ${surahId}`;

  return (
    <div className="surah-detail-page">
      <div className="surah-header">
        <button className="surah-back" onClick={onBack} aria-label="Back">← Back</button>
        <h2 className="surah-detail-title" dir="rtl">{surahName}</h2>
      </div>

      <div className="ayah-list">
        {ayahs.map(a => (
          <div className="ayah-card" key={a.ayah_id ?? a.original_id}>
            <div className="ayah-num">{a.ayah_id}</div>
            <div className="ayah-ar" lang="ar" dir="rtl">{a.arabic_text}</div>
            {a.english_text && <div className="ayah-en">{a.english_text}</div>}
          </div>
        ))}
      </div>
    </div>
  );
};

export default SurahDetail;
