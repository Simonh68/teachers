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
import { app, getAnonymousUser } from "../../../shared/firebase-anonymous-auth.js";
import { getFirestore, collection, doc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

// A refresh or switching between PeerJS and Firebase in the SAME tab is not
// another presentation launch. This flag stays only in the tab, not in Firebase.
const launchFlag = "teachers.grade12.sentence-detective.launch.logged.v1";
let alreadyLogged = false;
try { alreadyLogged = sessionStorage.getItem(launchFlag) === "1"; } catch {}
if (!new URLSearchParams(location.search).has("remote") && !alreadyLogged) {
  try {
    // Remote and analytics share the same technical anonymous Firebase identity.
    // No login is shown, and this identity is never written into the usage event.
    await getAnonymousUser();
    const ref = doc(collection(getFirestore(app), "teachersPresentationUsageV1"));
    await setDoc(ref, {
      deck: "grade12-sentence-detective",
      kind: "presentation-open",
      openedAt: serverTimestamp()
    });
    try { sessionStorage.setItem(launchFlag, "1"); } catch {}
    window.__teacherUsageLogged = true;
  } catch (error) {
    window.__teacherUsageLogged = false;
    // Logging is best-effort only; it must not interrupt a classroom lesson.
    console.warn("Anonymous presentation usage log unavailable:", error?.code || error);
  }
}
