"use client";

import { useState } from "react";
import { findings_, teams_ } from "./sidebar_";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPaperclip,
  faSmile,
  faMicrophoneAlt,
} from "@fortawesome/free-solid-svg-icons";

const Stage = () => {
  const [thumbnailExpanded, setThumbnailExpanded] = useState(false);
  const [generatedThumb, setGeneratedThumb] = useState("");

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      const videoId = new URL(e.target.value).searchParams.get("v");
      if (videoId) {
        setGeneratedThumb(`https://img.youtube.com/vi/${videoId}/0.jpg`);
        setThumbnailExpanded(true);
      } else {
        setGeneratedThumb("");
        alert("Please enter a valid YouTube video URL.");
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="flex flex-row items-center justify-center scale-[.90]">
        <div
          className={`w-[500px] ${
            thumbnailExpanded ? "h-[700px]" : "h-[100px]"
          } mx-2 transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center bg-white shadow-md relative`}
        >
          {!thumbnailExpanded && (
            <input
              type="text"
              placeholder="Enter YouTube video URL here"
              onKeyDown={handleKeyDown}
              className="w-full h-full border rounded p-2"
            />
          )}
          {thumbnailExpanded && (
            <div
              className={`bg-black rounded-[6px] w-full h-[200px] flex flex-col justify-center items-center overflow-hidden relative`}
            >
              <img className="w-full object-cover" src={generatedThumb} />
              <div
                className={`flex flex-row justify-center items-center absolute right-0 m-2`}
              ></div>
            </div>
          )}
          {thumbnailExpanded && (
            <div
              className={`flex flex-col justify-end items-center w-full h-[445px]`}
            >
              <div
                className={`flex flex-col justify-center items-center p-2 px-4 text-[14px] text-white/80 font-bold min-w-[80px] max-w-[250px] min-h-[30px] rounded-t-[6px] rounded-bl-[6px] bg-blue-400 ml-auto m-4`}
              >
                What do you think about this transcripts topic as a whole?
              </div>
              <div className={`mt-[-15px] ml-auto mr-[20px] text-[12px] text-black/50`}>
                10:24 - LwaziNF
              </div>
            </div>
          )}
          {thumbnailExpanded && (
            <div className="w-[98.3%] h-[40px] flex flex-row justify-center items-center rounded-[3px] bg-black/20 px-2 absolute bottom-2">
              <FontAwesomeIcon
                icon={faPaperclip}
                className={`mx-1 opacity-30`}
              />
              <input
                type="text"
                placeholder="Write a message"
                className="flex-grow px-2 bg-transparent outline-none text-white"
              />
              <FontAwesomeIcon icon={faSmile} className={`mx-1 opacity-30`} />
              <FontAwesomeIcon
                icon={faMicrophoneAlt}
                className={`mx-1 opacity-30`}
              />
            </div>
          )}
        </div>
        <div
          className={`${
            thumbnailExpanded ? "h-[700px] w-[500px]" : "h-[0px] w-[0px]"
          } transition-all duration-200 rounded-[6px] flex-col justify-evenly items-center mb-3`}
        >
          {[teams_, findings_].map((Component, idx) => (
            <div
              key={idx}
              className={`${
                thumbnailExpanded ? "w-full h-[49%]" : "w-0 h-0"
              } transition-all duration-200 rounded-[6px] p-1 m-2 flex-col justify-normal items-center bg-white shadow-md`}
            >
              {thumbnailExpanded && <Component />}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Stage;
