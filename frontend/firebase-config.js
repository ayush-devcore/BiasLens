import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { 
  getAuth, 
  GoogleAuthProvider, 
  TwitterAuthProvider, 
  GithubAuthProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged,
  signOut
  sendEmailVerification,
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import { getFirestore, doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-storage.js";

const firebaseConfig = {
  apiKey: "AIzaSyDD6gjNf9HMgTaie2Lv2xwouaq8AZDDjew",
  authDomain: "biaslens-3c517.firebaseapp.com",
  projectId: "biaslens-3c517",
  storageBucket: "biaslens-3c517.firebasestorage.app",
  messagingSenderId: "331810910970",
  appId: "1:331810910970:web:216943fbfec1e58ff74f43",
  measurementId: "G-25781WM3FT"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase services
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

// Authentication Providers
const googleProvider = new GoogleAuthProvider();
const twitterProvider = new TwitterAuthProvider();
const githubProvider = new GithubAuthProvider();

export { 
  app, 
  auth, 
  db, 
  storage,
  googleProvider,
  twitterProvider,
  githubProvider,
  signInWithPopup,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged,
  signOut,
  doc,
  setDoc,
  getDoc,
  ref,
  uploadBytes,
  getDownloadURL
};
