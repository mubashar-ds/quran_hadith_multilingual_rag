import React from 'react';

const Collections = ({ onSelect }) => {
  return (
    <section className="choice-buttons">
      <button
        className="choice-button"
        onClick={() => (onSelect ? onSelect('quran') : console.log('Quran'))}
      >
        Quran
      </button>

      <button
        className="choice-button"
        onClick={() => (onSelect ? onSelect('hadit') : console.log('Hadit'))}
      >
        Hadit
      </button>
    </section>
  );
};

export default Collections;
