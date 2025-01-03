'use client'

import { faAngleDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

const Stage = () => {
    const [expandThumb_, setExpandThumb_] = useState(true)
  return (
    <div className={`flex flex-col items-center justify-center`}>
      <div
        className={`w-[500px] h-[700px] transition-all duration-200 rounded-[6px] p-1 flex-col justify-normal items-center bg-white shadow-md`}
      >
        <div
          className={`w-full ${expandThumb_ ? 'h-[200px]' : 'h-[50px]'} transition-all duration-200 flex flex-row justify-start items-end rounded-t-[6px] rounded-b-[3px] bg-black/45`}
        >
            <div className={`w-[45px] h-[15px] bg-white rounded-[2px] m-1 flex-col justify-center items-center flex p-1 cursor-pointer`} onClick={() => {
                setExpandThumb_(!expandThumb_)
            }}></div>
            <div className={`w-[15px] h-[15px] bg-white rounded-[2px] m-1 flex-col justify-center items-center flex p-1 cursor-pointer`} onClick={() => {
                setExpandThumb_(!expandThumb_)
            }}>
                <FontAwesomeIcon icon={faAngleDown} className={`text-black ${expandThumb_ ? 'rotate-180' : 'rotate-0'}`}/>
            </div>
        </div>
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
