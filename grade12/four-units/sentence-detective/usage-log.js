/**
 * Minimal anonymous presentation-launch log.
 * This counts launches, NOT distinct teachers. Reloads can count again.
 * Excludes QR phone controllers to avoid double-counting one presentation.
 * Writes only deck ID, event type and a server timestamp; never writes UID,
 * email, name, phone number, IP, or any browser fingerprint.
 *
 * Requires Anonymous Authentication and the narrowly scoped rules described in
 * FIREBASE_RULES_FRAGMENT.txt. Failure never blocks the presentation.
 */
import { firebaseConfig } from "../../../shared/firebase-config.js";
import { initializeApp, getApp, getApps } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getAuth, signInAnonymously } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";
import { getFirestore, collection, doc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

if (!new URLSearchParams(location.search).has("remote")) {
  try {
    const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
    const auth = getAuth(app);
    await auth.authStateReady();
    // Reuse the anonymous Firebase technical identity when present.
    // This never requests a user-visible login or saves the identity to the usage log.
    if (!auth.currentUser) await signInAnonymously(auth);
    const ref = doc(collection(getFirestore(app), "teachersPresentationUsageV1"));
    await setDoc(ref, {
      deck: "grade12-sentence-detective",
      kind: "presentation-open",
      openedAt: serverTimestamp()
    });
  } catch (error) {
    // Logging is best-effort only; it must not interrupt a classroom lesson.
    console.warn("Anonymous presentation usage log unavailable:", error?.code || error);
  }
}
