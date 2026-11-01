/**
 * Shared public Firebase Web App configuration for teaching presentations.
 * This is the web application identity, NOT a service account or secret.
 * Project: vocabdev-56392 (project number 858434938577).
 *
 * Import in future HTML presentation modules:
 *   import { firebaseConfig } from "../../../shared/firebase-config.js";
 *
 * Security: Firebase Auth, Security Rules and optionally App Check must enforce
 * access permissions. Do not enable public database writes just to test pairing.
 */
export const firebaseConfig = Object.freeze({
  apiKey: "AIzaSyCyG6Bmev35AcFQ7lJluHjRwMYrSa_a2nI",
  authDomain: "vocabdev-56392.firebaseapp.com",
  projectId: "vocabdev-56392",
  storageBucket: "vocabdev-56392.firebasestorage.app",
  messagingSenderId: "858434938577",
  appId: "1:858434938577:web:e18d043bc99449383a47f0"
});
