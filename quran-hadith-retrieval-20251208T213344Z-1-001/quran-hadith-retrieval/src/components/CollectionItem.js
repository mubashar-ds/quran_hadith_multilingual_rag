import React from 'react';

const CollectionItem = ({ item }) => {
  return (
    <div className="collection-item" role="button" tabIndex={0}>
      <div className="collection-en">{item.en}</div>
      <div className="collection-ar">{item.ar}</div>
    </div>
  );
};

export default CollectionItem;
