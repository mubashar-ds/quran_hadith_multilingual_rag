import React from 'react';
import HadithData from '../dataset/Sahih_Bukhari_Dataset.json';
import './HadithList.css';

const HadithList = ({ onBack, onSelectCollection }) => {
  const map = new Map();
  HadithData.forEach(item => {
    const id = item.chapter_id ?? item.chapter_id === 0 ? String(item.chapter_id) : (item.chapter_name_ar || 'unknown');
    if (!map.has(id)) {
      map.set(id, {
        id,
        name_ar: item.chapter_name_ar || item.chapter_name_en || id,
        name_en: item.chapter_name_en || '',
      });
    }
  });
  const collections = Array.from(map.values());

  return (
    <div className="hadith-page">
      <div className="hadith-header">
        <button className="hadith-back" onClick={onBack} aria-label="Back">← Back</button>
        <h2>احادیث جات</h2>
      </div>

      <div className="hadith-grid">
        {collections.map((c, idx) => (
          <button key={c.id} className="hadith-card" onClick={() => onSelectCollection(c.id)}>
            <div className="hadith-num">{idx + 1}</div>
            <div className="hadith-name-ar" dir="rtl">{c.name_ar}</div>
            {c.name_en && <div className="hadith-name-en">{c.name_en}</div>}
          </button>
        ))}
      </div>
    </div>
  );
};

export default HadithList;
