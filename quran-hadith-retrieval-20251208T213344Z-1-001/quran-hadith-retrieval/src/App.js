import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import Collections from './components/Collections';
import Footer from './components/Footer';
import SurahList from './components/SurahList';
import SurahDetail from './components/SurahDetail';
import HadithList from './components/HadithList';
import HadithDetail from './components/HadithDetail';
import SearchResults from './components/SearchResults';

function App() {
  const [selection, setSelection] = useState(null);
  const [view, setView] = useState(null);
  const [currentSurahId, setCurrentSurahId] = useState(null);
  const [currentHadithCollection, setCurrentHadithCollection] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [isSearching, setIsSearching] = useState(false);

  function handleSelect(name) {
    setSelection(name);
    console.log('Selected:', name);
  }

  async function handleSearch(query) {
    if (!query.trim()) return;
    
    setIsSearching(true);
    console.log('🔍 Starting search for:', query);
    
    // Use CORS proxy
    const API_URL = 'https://corsproxy.io/?https://sagaciously-punchy-sheree.ngrok-free.dev';
    // OR use another proxy:
    // const API_URL = 'https://api.allorigins.win/raw?url=https://sagaciously-punchy-sheree.ngrok-free.dev';
    
    try {
      console.log('📤 Making API call via CORS proxy');
      
      const response = await fetch(`${API_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: query,
          top_k: 5,
          source: 'both'
        })
      });
      
      console.log('📡 Response status:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('✅ Search successful!');
        setSearchResults(data);
      } else {
        const errorText = await response.text();
        console.error('❌ Search failed:', response.status, errorText);
      }
    } catch (error) {
      console.error('🚨 Search error:', error);
    } finally {
      setIsSearching(false);
      console.log('🏁 Search process completed');
    }
  }

  useEffect(() => {
    if (!selection) return;
    const t = setTimeout(() => setSelection(null), 3000);
    return () => clearTimeout(t);
  }, [selection]);

  return (
    <div className="App site-root">
      <Header 
        onQuranClick={() => setView('surahList')}
        onHadithClick={() => setView('hadithList')}
      />

      <main className="main-content">
        {view === null && (
          <div className="hero">
            <h1 className="hero-title" style={{textAlign: 'center'}}>
              SEARCH QURAN & HADITH
              <br />
              <span style={{fontSize: '0.5em', fontWeight: 300, letterSpacing: '0.5px'}}>
                authoritative collections with fast retrievals
              </span>
            </h1>

            <SearchBar onSearch={handleSearch} />
            
            {isSearching && (
              <div style={{marginTop: '16px', color: '#61b6b0', fontWeight: 600}}>
                Searching...
              </div>
            )}
            
            <div className="toggle-row">
              <button
                className={`pill ${selection === 'quran' ? 'active' : ''}`}
                onClick={() => setView('surahList')}
              >
                Quran
              </button>

              <button
                className={`pill ${selection === 'hadit' ? 'active' : ''}`}
                onClick={() => setView('hadithList')}
              >
                Hadith
              </button>
            </div>
          </div>
        )}

        {view === 'surahList' ? (
          <SurahList 
            onBack={() => setView(null)} 
            onSelectSurah={(id) => { 
              setCurrentSurahId(id); 
              setView('surahDetail'); 
            }} 
          />
        ) : null}

        {view === 'surahDetail' && (
          <SurahDetail 
            surahId={currentSurahId} 
            onBack={() => setView('surahList')} 
          />
        )}

        {view === 'hadithList' ? (
          <HadithList 
            onBack={() => setView(null)} 
            onSelectCollection={(cid) => { 
              setCurrentHadithCollection(cid); 
              setView('hadithDetail'); 
            }} 
          />
        ) : null}

        {view === 'hadithDetail' && (
          <HadithDetail 
            collectionId={currentHadithCollection} 
            onBack={() => setView('hadithList')} 
          />
        )}
      </main>

      {!(view === 'surahList' || view === 'surahDetail' || view === 'hadithList' || view === 'hadithDetail') && (
        <Footer />
      )}

      {selection && (
        <div className="selection-floating" role="status" aria-live="polite">
          You selected: <strong>{selection}</strong>
        </div>
      )}

      {searchResults && (
        <SearchResults 
          results={searchResults} 
          onClose={() => {
            console.log('🗑️ Closing search results');
            setSearchResults(null);
          }} 
        />
      )}
    </div>
  );
}

export default App;