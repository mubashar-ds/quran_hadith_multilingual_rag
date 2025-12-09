import React from 'react';

const Header = ({ onQuranClick, onHadithClick }) => {
  return (
    <header className="site-header">
      <div className="page-topbar">
        <div className="topbar-inner">
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div className="logo-mark">✦</div>
            <div style={{ display: 'flex', flexDirection: 'column', marginLeft: 10 }}>
              <div className="brand">Quran & Hadith</div>
            </div>
          </div>

          <nav className="topbar-nav">
            <a href="#" onClick={(e) => { e.preventDefault(); onQuranClick(); }}>Quran</a>
            <a href="#" onClick={(e) => { e.preventDefault(); onHadithClick(); }}>Hadith</a>
            <a href="#">Prayer Time</a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
