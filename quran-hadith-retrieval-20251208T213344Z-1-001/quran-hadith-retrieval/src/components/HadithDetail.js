import React from 'react';
import HadithData from '../dataset/Sahih_Bukhari_Dataset.json';
import './HadithDetail.css';

const HadithDetail = ({ collectionId, onBack }) => {
  if (!collectionId) return null;

  const items = HadithData.filter(
    item => String(item.chapter_id) === String(collectionId)
  );
  const chapterNameAr = items.length ? items[0].chapter_name_ar : collectionId;

  return (
    <div className="hadith-detail-page">
      <div className="hadith-detail-header">
        <button className="hadith-back" onClick={onBack}>← Back</button>
        <h2 className="hadith-detail-title" dir="rtl">{chapterNameAr}</h2>
      </div>

      <div className="hadith-list">
        {items.map(h => (
          <div className="hadith-detail-card" key={h.doc_id}>
            <div className="hadith-num">{h.hadith_id}</div>
            <div className="hadith-ar" dir="rtl">{h.arabic_text}</div>
            {h.english_text && (
              <div className="hadith-en">{h.english_text}</div>
            )}
            {h.narrator && (
              <div className="hadith-narrator">Narrator: {h.narrator}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default HadithDetail;
