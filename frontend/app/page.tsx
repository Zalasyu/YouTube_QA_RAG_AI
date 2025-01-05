"use client"

import { signOut_, useAuth } from "@/firebase";
import LoginPage from "./components/auth/LoginForm";
import Stage from "./components/Stage";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPowerOff } from "@fortawesome/free-solid-svg-icons";

export default function Home() {
  const { currentUser, isUserActive } = useAuth();

  return (
    <>
      {isUserActive ? <div className={`flex flex-col justify-center items-center`}>
      <Stage />
      <div className={`w-[80px] h-[30px] rounded-[3px] bg-white absolute top-2 right-2 justify-center items-center flex flex-row p-1 cursor-pointer`} onClick={() => {
        signOut_()
      }} >
        <FontAwesomeIcon icon={faPowerOff} className={`text-[12px] mr-1`} />
        <p className={`text-[12px] font-medium`}>
        Signout
        </p>
      </div>
      </div> : <LoginPage />}
    </>
  );
}