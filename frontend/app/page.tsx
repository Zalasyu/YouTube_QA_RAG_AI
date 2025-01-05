"use client"

import { useAuth } from "@/firebase";
import LoginPage from "./components/auth/LoginForm";
import Stage from "./components/Stage";

export default function Home() {
  const { currentUser, isUserActive } = useAuth();

  return (
    <>
      {isUserActive ? <Stage /> : <LoginPage />}
    </>
  );
}