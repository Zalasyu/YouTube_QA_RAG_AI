import { initializeApp } from "firebase/app";
import {
  GoogleAuthProvider,
  createUserWithEmailAndPassword,
  getAuth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
} from "firebase/auth";
import {
  collection,
  doc,
  getDocs,
  getFirestore,
  orderBy,
  query,
  setDoc,
  where,
} from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";
import { useEffect, useState } from "react";
import { v4 } from "uuid";

const firebaseConfig = {
  apiKey:  process.env.API_KEY,
  authDomain: "agency-23b74.firebaseapp.com",
  projectId: "agency-23b74",
  storageBucket: "agency-23b74.firebasestorage.app",
  messagingSenderId: "904152769359",
  appId: "1:904152769359:web:666a8b475579bd2f565b3a",
  measurementId: "G-L7F22LJYB6"
};

const app = initializeApp(firebaseConfig);
let analytics;
if (typeof window !== "undefined") {
  analytics = getAnalytics(app);
}
const auth = getAuth(app);
const db = getFirestore(app);
const store = getStorage(app);
const provider = new GoogleAuthProvider();

export { db, store, auth, analytics };

export const getMessages = async () => {
    // Get a reference to the "messages" collection
    const colRef = collection(db, "messages");
  
    // Fetch the documents in the collection
    const querySnapshot = await getDocs(colRef);
  
    // Map over the documents and return their data with the document ID
    return querySnapshot.docs.map((doc) => ({
      ...doc.data(),
      id: doc.id,
    }));
  };

export const signIn_ = async () => {
  return signInWithPopup(auth, provider).then((data) => {});
};

export const signOut_ = () => {
  return signOut(auth);
};

export const useAuth = () => {
  const [currentUser_, setCurrentUser_] = useState();

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (user) => setCurrentUser_(user));
    return unsub;
  }, []);
  return currentUser_;
};