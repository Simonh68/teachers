/**
 * Firebase Auth for public HTML teaching presentations.
 * No teacher sign-up, email or profile is requested.
 * Firebase issues a temporary technical anonymous UID for access control;
 * it is NOT included in presentation usage logs.
 *
 * Share one initialization promise across remote control and usage logging:
 * concurrent signInAnonymously() calls can otherwise create different UIDs.
 */
import { firebaseConfig } from "./firebase-config.js";
import { initializeApp, getApp, getApps } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getAuth, signInAnonymously } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

export const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
export const auth = getAuth(app);

export function getAnonymousUser() {
  if (!window.__teachersFirebaseAuthPromise) {
    window.__teachersFirebaseAuthPromise = (async () => {
      await auth.authStateReady();
      if (auth.currentUser) return auth.currentUser;
      return (await signInAnonymously(auth)).user;
    })().catch(error => {
      window.__teachersFirebaseAuthPromise = null;
      throw error;
    });
  }
  return window.__teachersFirebaseAuthPromise;
}
