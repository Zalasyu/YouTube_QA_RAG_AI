"use client";

import { useState } from 'react';

const Stage = () => {
  const [thumbnailExpanded, setThumbnailExpanded] = useState(false);

  const toggleExpand = () => {
    setThumbnailExpanded(!thumbnailExpanded);
  };

  return (
    <div className="flex flex-row items-center justify-center scale-[.90]">
      <div
        onClick={toggleExpand}
        className={`w-[500px] ${thumbnailExpanded ? 'h-[700px]' : 'h-[100px]'} mx-2 transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center bg-white shadow-md`}
      >
      </div>
      <div
        className={`${thumbnailExpanded ? 'h-[700px] w-[500px]' : 'h-[0px] w-[0px]'} transition-all duration-200 rounded-[6px] flex-col justify-evenly items-center mb-3`}
      >
       {
        [1, 2].map((obj_, idx_) => {
          return (<div
          key={idx_}
            className={`${thumbnailExpanded ? 'w-full h-[49%]' : 'w-0 h-0'} transition-all duration-200 rounded-[6px] p-1 m-2 flex-col justify-normal items-center bg-white shadow-md`}
          >
            
          </div>)
        })
       } 
      </div>
    </div>
  );
};

export default Stage;