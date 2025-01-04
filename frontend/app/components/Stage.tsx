"use client";

import { useState } from "react";

const Stage = () => {
  const [expandThumb_, setExpandThumb_] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [thumbnail, setThumbnail] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      setLoading(true);
      setError('');
      setInputValue(''); // Clear the input value

      // Extract video ID from the URL
      const url = new URL(inputValue);
      let videoId = '';
      
      if (url.hostname === 'www.youtube.com' || url.hostname === 'youtube.com') {
        const searchParams = new URLSearchParams(url.search);
        videoId = searchParams.get('v');
      } else if (url.hostname === 'youtu.be') {
        videoId = url.pathname.slice(1);
      }

      if (videoId) {
        // Generate thumbnail URL
        const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
        setTimeout(() => {
          setThumbnail(thumbnailUrl); // Set the thumbnail URL
          setExpandThumb_(true); // Expand the thumbnail
          setLoading(false);
        }, 1000); // Simulating API call delay
      } else {
        setTimeout(() => {
          setError('Could not extract video ID from the URL');
          setLoading(false);
        }, 1000); // Simulating API call delay for error case
      }
    }
  };

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  return (
    <div className="flex flex-col items-center justify-center">
      <div
        className={`w-[500px] h-[700px] transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center bg-white shadow-md`}
      >
        <div
          className={`w-full ${expandThumb_ ? "h-[200px]" : "h-[50px]"} relative overflow-hidden transition-all duration-200 flex flex-row justify-end items-start rounded-t-[6px] rounded-b-[3px] bg-black/45`}
        >
          {loading ? (
            <div className="w-full h-full flex justify-center items-center">
              <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-white"></div>
            </div>
          ) : thumbnail ? (
            <img className={`h-full w-full object-cover`} src={thumbnail} alt="YouTube Thumbnail" />
          ) : null}
          <input
            type="text"
            value={inputValue}
            onChange={handleChange}
            onKeyPress={handleKeyPress}
            placeholder="Enter your desired Youtube link.."
            className={`w-full h-full absolute rounded-[2px] bg-transparent ${expandThumb_ ? "opacity-0 pointer-events-none" : "opacity-100 pointer-events-auto"} flex-col justify-center items-center flex p-1 text-center cursor-pointer`}
          />
        </div>
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        <div className={`w-full h-[1px] rounded-[3px] my-2 px-2`}>
          <div className={`w-full h-[1px] rounded-[3px] bg-black/45`} />
        </div>
        <div className={`w-full h-[40px] rounded-[3px] my-1 bg-black/45`}></div>
        <div className={`w-full h-[1px] rounded-[3px] my-2 px-2`}>
          <div className={`w-full h-[1px] rounded-[3px] bg-black/45`} />
        </div>
      </div>
    </div>
  );
};

export default Stage;