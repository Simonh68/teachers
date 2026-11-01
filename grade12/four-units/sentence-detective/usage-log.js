/**
 * Minimal anonymous presentation-launch log.
 * This counts presenter-tab launches, NOT distinct teachers. Reloads in the same tab are ignored.
 * Excludes QR phone controllers to avoid double-counting one presentation.
 * Writes only deck ID, event type and a server timestamp; never writes UID,
 * email, name, phone number, IP, or any browser fingerprint.
 *
 * Requires anonymous technical Firebase authorization and the scoped rules at
 * firebase-backend/firestore.rules. Failure never blocks the presentation.
 */
import { app, getAnonymousUser } from "../../../shared/firebase-anonymous-auth.js";
import { getFirestore, collection, doc, writeBatch, increment, serverTimestamp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

// A refresh or switching between PeerJS and Firebase in the SAME tab is not
// another presentation launch. This flag stays only in the tab, not in Firebase.
const launchFlag = "teachers.grade12.sentence-detective.launch.logged.v1";
let alreadyLogged = false;
try { alreadyLogged = sessionStorage.getItem(launchFlag) === "1"; } catch {}
const query = new URLSearchParams(location.search);
// Explicit QA preview does not inflate the real teaching usage report.
if (!query.has("remote") && !query.has("qa") && !alreadyLogged) {
  try {
    // Remote and analytics share the same technical anonymous Firebase identity.
    // No login is shown, and this identity is never written into the usage event.
    await getAnonymousUser();
    const db = getFirestore(app);
    const event = doc(collection(db, "teachersPresentationUsageV1"));
    const stats = doc(db, "teachersPresentationStatsV1", "grade12-sentence-detective");
    // Atomic event + aggregate update: the displayed count matches the log.
    // Neither document contains the Firebase UID or other user details.
    const batch = writeBatch(db);
    batch.set(event, {
      deck: "grade12-sentence-detective",
      kind: "presentation-open",
      openedAt: serverTimestamp()
    });
    batch.set(stats, {
      deck: "grade12-sentence-detective",
      opens: increment(1),
      updatedAt: serverTimestamp(),
      lastEventId: event.id
    }, { merge: true });
    await batch.commit();
    try { sessionStorage.setItem(launchFlag, "1"); } catch {}
    window.__teacherUsageLogged = true;
  } catch (error) {
    window.__teacherUsageLogged = false;
    // Logging is best-effort only; it must not interrupt a classroom lesson.
    console.warn("Anonymous presentation usage log unavailable:", error?.code || error);
  }
}
