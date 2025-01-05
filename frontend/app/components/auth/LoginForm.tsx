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

export default function LoginPage() {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

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
      router.push("/"); // Redirect to the main page (page.tsx)
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
      router.push("/"); // Redirect to the main page (page.tsx)
    } catch (err: any) {
      setError(err.message);
      console.error("Google sign-in error:", err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="text-white mb-10">
          <h1 className="text-5xl font-extrabold mb-2">Welcome to Zentrix</h1>
          <p className="text-lg font-medium">Log in to get the best experience</p>
        </div>

        <div className="bg-white shadow-xl rounded-lg p-8 w-full max-w-md">
          <h2 className="text-3xl font-semibold text-center mb-6">
            {isSignUp ? "Sign Up" : "Login"}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition duration-200"
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
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none transition duration-200"
                placeholder="Enter your password"
              />
            </div>
            {error && (
              <div className="text-red-600 text-sm text-center">{error}</div>
            )}
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition duration-200"
            >
              {isSignUp ? "Sign Up" : "Login"}
            </button>
          </form>
          <button
            onClick={handleGoogleSignIn}
            className="mt-4 w-full bg-red-600 text-white py-3 rounded-lg font-medium hover:bg-red-700 transition duration-200"
          >
            Sign in with Google
          </button>
          <div className="text-center mt-6">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
            <button
              onClick={toggleAuthMode}
              className="text-blue-600 hover:underline"
            >
              {isSignUp ? "Login" : "Sign Up"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
