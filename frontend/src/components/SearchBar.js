import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
  const [value, setValue] = useState('');

  function submit() {
    console.log('🔍 SearchBar: Submitting query:', value.trim());
    if (onSearch) onSearch(value.trim());
  }

  function onKey(e) {
    if (e.key === 'Enter') submit();
  }

  return (
    <div className="search-wrap">
      <div className="search-box">
        <input
          className="search-input"
          type="text"
          placeholder="Search anything about quran and hadees"
          aria-label="Search"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={onKey}
          style={{textAlign: 'center'}}
        />
        <button className="search-btn" aria-label="Search" onClick={submit}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2 12L22 3L10 13L14 22L2 12Z" fill="currentColor"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default SearchBar;