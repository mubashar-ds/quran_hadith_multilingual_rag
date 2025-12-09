import React from 'react';

const Footer = () => {
  return (
    <footer className="site-footer">
      <div className="footer-inner">
        <div className="footer-links">
          <a href="#">About</a>
          <a href="#">Contact</a>
          <a href="#">Privacy</a>
        </div>
        <div className="footer-copy">© {new Date().getFullYear()} Quran_Hadit Retrieval system</div>
      </div>
    </footer>
  );
};

export default Footer;
