import React from 'react';
import QuranData from '../dataset/AL_Quran_Dataset.json';
import './SurahList.css';

const buildSurahList = () => {
  const map = new Map();
  for (const item of QuranData) {
    if (!map.has(item.surah_id)) {
      map.set(item.surah_id, {
        id: item.surah_id,
        name_ar: item.surah_name_ar,
        name_en: item.surah_name_en,
      });
    }
  }
  return Array.from(map.values()).sort((a,b) => a.id - b.id);
};

const SurahList = ({ onBack, onSelectSurah }) => {
  const surahs = buildSurahList();

  return (
    <div className="surah-page">
      <div className="surah-header">
        <button className="surah-back" onClick={onBack} aria-label="Back">← Back</button>
        <h2>سورہ جات</h2>
      </div>

      <div className="surah-grid">
        {surahs.map(s => (
          <button key={s.id} className="surah-card" onClick={() => onSelectSurah ? onSelectSurah(s.id) : null}>
            <div className="surah-num">{s.id}</div>
            <div className="surah-name-ar">{s.name_ar}</div>
            <div className="surah-name-en">{s.name_en}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default SurahList;
