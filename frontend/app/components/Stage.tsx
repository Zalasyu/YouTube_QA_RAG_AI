"use client";

import { useState } from 'react';

const Stage = () => {
  const [thumbnailExpanded, setThumbnailExpanded] = useState(false);

  const toggleExpand = () => {
    setThumbnailExpanded(!thumbnailExpanded);
  };

  return (
    <div className="flex flex-row items-center justify-center">
      <div
        onClick={toggleExpand}
        className={`w-[500px] ${thumbnailExpanded ? 'h-[700px]' : 'h-[100px]'} mx-2 transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center bg-white shadow-md`}
      >
      </div>
      <div
        onClick={toggleExpand}
        className={`${thumbnailExpanded ? 'h-[700px] w-[500px]' : 'h-[0px] w-[0px]'} transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center`}
      >
        
      </div>
    </div>
  );
};

export default Stage;