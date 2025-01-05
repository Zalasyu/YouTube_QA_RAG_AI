export const teams_ = () => {
    return ( 
        <div className={``}>
            teams_
        </div>
     );
}

export const findings_ = () => {
    return ( 
        <div className={`w-full h-full flex flex-col justify-start items-center`}>
            <div className={`w-full min-h-2 flex flex-row justify-center items-center`}>
                {['Transcript', 'Bookmarks', 'Take Aways'].map((obj_, idx_) => {
                    return <div key={idx_} className={`w-[100px] h-[30px] flex flex-col justify-center items-center text-black/70 hover:text-white/70 text-[14px] font-semibold m-1 rounded-[3px] bg-black/15 hover:bg-black/30 transition-all duration-200 cursor-pointer`}>
                        {obj_}
                    </div>
                })}
            </div>
            
        </div>
     );
}
 