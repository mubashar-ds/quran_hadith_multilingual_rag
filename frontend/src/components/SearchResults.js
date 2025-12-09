import React, { useEffect } from 'react';
import './SearchResults.css';

const SearchResults = ({ results, onClose }) => {
  useEffect(() => {
    if (results) {
      console.log('🎯 SearchResults: Rendering with data');
      console.log('📊 Results from backend:', results);
    }
  }, [results]);

  if (!results) {
    console.log('🚫 No results to display');
    return null;
  }

  return (
    <div className="search-results-overlay" onClick={onClose}>
      <div className="search-results-container" onClick={(e) => e.stopPropagation()}>
        <div className="search-results-header">
          <h2>Search Results for: "{results.query}"</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="search-results-content">
          {(results.top_results?.length === 0) ? (
            <p className="no-results">No results found</p>
          ) : (
            <>
              <div className="results-summary">
                <p>Found {results.top_results?.length || 0} results</p>
              </div>

              <div className="results-list">
                {results.top_results?.map((result, index) => (
                  <div key={index} className="result-card">
                    <div className="result-header">
                      <span className="result-source">
                        {result.source === 'quran' ? 'قرآن' : 
                         result.source === 'hadith' ? 'حدیث' : 'قرآن'}
                      </span>
                    </div>

                    <div className="result-info">
                      <span>{result.surah_name_ar || result.surah_name_en || result.collection_name} 
                      {result.ayah_id ? ` - آیت ${result.ayah_id}` : ''}
                      {result.hadith_id ? ` - حدیث ${result.hadith_id}` : ''}</span>
                    </div>

                    <div className="result-text arabic" dir="rtl">
                      {result.arabic_text}
                    </div>

                    {result.urdu_text && (
                      <div className="result-text urdu" dir="rtl">
                        <strong>اردو:</strong> {result.urdu_text}
                      </div>
                    )}

                    <div className="result-text english">
                      <strong>English:</strong> {result.english_text}
                    </div>

                    {result.narrator && (
                      <div className="result-narrator">
                        <em>Narrator: {result.narrator}</em>
                      </div>
                    )}

                    <div className="result-score">
                      <small>Relevance Score: {result.score?.toFixed(4) || 'N/A'}</small>
                    </div>
                  </div>
                ))}
              </div>

              {results.llm_explanation && (
                <div className="explanation-section">
                  <h3>تفصیلی وضاحت</h3>
                  <div className="explanation-text" dir="rtl">
                    {results.llm_explanation.urdu.split('\n').map((line, i) => {
                      const parts = line.split(/(\*.*?\*)/g);
                      return (
                        <p key={i}>
                          {parts.map((part, j) => {
                            if (part.startsWith('*') && part.endsWith('*') && part.length > 2) {
                              return <strong key={j}>{part.slice(1, -1)}</strong>;
                            }
                            return <span key={j}>{part}</span>;
                          })}
                        </p>
                      );
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchResults;