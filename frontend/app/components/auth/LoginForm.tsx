"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation"; // For routing
import { auth } from "../../../firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
import { signOut_ } from "../../../firebase"; // Import signOut function
import { useAuth } from "../../../firebase"; // Import custom useAuth hook

export default function LoginForm() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter(); // Hook for routing

  const { currentUser, isUserActive, isLoading } = useAuth(); // Get user status

  const toggleAuthMode = () => {
    setIsSignUp((prev) => !prev);
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      if (isSignUp) {
        await createUserWithEmailAndPassword(auth, email, password);
        console.log("Sign-up successful!");
      } else {
        await signInWithEmailAndPassword(auth, email, password);
        console.log("Login successful!");
      }
      router.push("/"); // Redirect to the main page
    } catch (err: any) {
      setError(err.message);
      console.error("Authentication error:", err);
    }
  };

  const handleGoogleSignIn = async () => {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
      console.log("Google sign-in successful!");
      router.push("/"); // Redirect to the main page
    } catch (err: any) {
      setError(err.message);
      console.error("Google sign-in error:", err);
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut_();
      console.log("Sign-out successful!");
      router.push("/login"); // Redirect to the login page after sign-out
    } catch (err: any) {
      setError(err.message);
      console.error("Sign-out error:", err);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-sm mt-8">
        {isLoading ? (
          <p>Loading...</p>
        ) : isUserActive ? (
          <div className="text-center">
            <h2 className="text-2xl font-semibold mb-4">
              Welcome, {currentUser?.email || "User"}!
            </h2>
            <button
              onClick={handleSignOut}
              className="w-full bg-red-600 text-white py-2 rounded-md hover:bg-red-700 transition duration-200"
            >
              Sign Out
            </button>
          </div>
        ) : (
          <>
            <h2 className="text-2xl font-semibold text-center mb-4">
              {isSignUp ? "Sign Up" : "Login"}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="Enter your email"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Password
                </label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
                  placeholder="Enter your password"
                />
              </div>
              {error && <div className="text-red-500 text-sm mt-2">{error}</div>}
              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-200"
              >
                {isSignUp ? "Sign Up" : "Login"}
              </button>
            </form>
            <button
              onClick={handleGoogleSignIn}
              className="mt-4 w-full bg-red-600 text-white py-2 rounded-md hover:bg-red-700 transition duration-200"
            >
              Sign in with Google
            </button>
            <div className="text-center mt-4">
              {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
              <button
                onClick={toggleAuthMode}
                className="text-blue-500 hover:underline"
              >
                {isSignUp ? "Login" : "Sign Up"}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
