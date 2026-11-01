/**
 * Sentence Detective — OPTIONAL Firebase/Firestore remote.
 * Activate only with ?sync=firebase; the existing PeerJS remote remains default.
 * Public web config lives in ../../../shared/firebase-config.js.
 * Requires Firebase Anonymous Authentication and NARROW Firestore security rules.
 * Never modify or replace the English for Noar production rules in order to run this.
 */
import { firebaseConfig } from "../../../shared/firebase-config.js";
import { initializeApp, getApps, getApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getAuth, signInAnonymously, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";
import {
  getFirestore, collection, doc, getDoc, setDoc, updateDoc, deleteDoc,
  onSnapshot, serverTimestamp, Timestamp
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

const COLLECTION = "teachersPresentationRemoteV1";
const DECK_ID = "grade12-sentence-detective";
const urlParams = new URLSearchParams(location.search);
const sessionId = urlParams.get("remote");
const isController = !!sessionId;
const $ = id => document.getElementById(id);
const remote = {
  role: isController ? "controller" : "presenter",
  transport: "firebase",
  connected: false,
  applying: false,
  pending: null,
  sessionRef: null,
  user: null,
  lastSignature: "",
  unsubscribers: [],
  broadcast: () => {},
  canNavigate: () => !isController || remote.connected,
  syncUi: () => {}
};
window.deckRemote = remote;
document.body.classList.add(isController ? "remote-controller" : "remote-presenter");
const dialog = $("pairDialog"), approveButton = $("pairApprove"), resetButton = $("pairReset");
const badge = $("syncBadge"), pairStatus = $("pairStatus");
const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
let writeChain = Promise.resolve();
let initializing = false;

function announce(message, tone = "waiting") {
  badge.textContent = message;
  badge.dataset.tone = tone;
  if (!isController) pairStatus.textContent = message;
}
function explain(error) {
  const code = String(error?.code || "");
  if (code.includes("operation-not-allowed")) return "Firebase: יש להפעיל את ספקי Google וכניסה אנונימית ב-Authentication.";
  if (code.includes("unauthorized-domain")) return "Firebase: יש להוסיף את simonh68.github.io לדומיינים המורשים ל-Authentication.";
  if (code.includes("permission-denied") || code.includes("insufficient-permissions"))
    return "Firebase: כללי Firestore עדיין אינם מאפשרים את אזור השלט; אין לשנות את הרשאות English for Noar.";
  if (code.includes("not-found") || code.includes("failed-precondition"))
    return "Firebase: מסד Firestore אינו מוכן או אינו קיים בפרויקט.";
  if (code.includes("network") || code.includes("unavailable"))
    return "Firebase: אין כרגע חיבור לרשת. אפשר לחזור לשלט הרגיל.";
  return "Firebase: " + (code || "לא ניתן להתחבר כרגע");
}
function handleError(error) {
  console.error("Firebase presentation remote:", error);
  remote.connected = false;
  announce(explain(error), "error");
  refreshUi();
}
function valueSnapshot() {
  return {
    index: state.index,
    stage: state.stage,
    selected: Object.assign({}, state.selected)
  };
}
function clean(data) {
  if (!data || !Number.isInteger(data.index) || data.index < 0 || data.index >= slides.length ||
      !Number.isInteger(data.stage) || data.stage < 0 || data.stage > 4 ||
      !data.selected || Array.isArray(data.selected) || typeof data.selected !== "object") return null;
  const selected = {};
  for (const [key, value] of Object.entries(data.selected)) {
    const i = Number(key);
    if (Number.isInteger(i) && i >= 0 && i < slides.length && Number.isInteger(value) &&
        value >= 0 && value < (slides[i].choices || []).length) selected[i] = value;
  }
  return {index: data.index, stage: data.stage, selected};
}
function signature(data) {
  return JSON.stringify([data.index, data.stage, data.selected]);
}
function applyRemote(data) {
  const valid = clean(data);
  if (!valid || signature(valid) === signature(valueSnapshot())) return;
  remote.applying = true;
  try {
    state.index = valid.index;
    state.stage = valid.stage;
    state.selected = valid.selected;
    remote.lastSignature = signature(valid);
    render();
  } finally {
    remote.applying = false;
  }
}
function refreshUi() {
  if (!isController) return;
  $("prev").disabled = !remote.connected || state.index === 0;
  $("next").disabled = !remote.connected || state.index === slides.length - 1;
  $("reveal").disabled = !remote.connected;
  $("reset").disabled = !remote.connected ||
    (state.stage === 0 && state.selected[state.index] === undefined);
  document.querySelectorAll("[data-choice]").forEach(btn => { btn.disabled = !remote.connected; });
}
remote.syncUi = refreshUi;
remote.broadcast = () => {
  if (!remote.sessionRef || !remote.user || remote.applying || (isController && !remote.connected)) return;
  const stateData = valueSnapshot();
  const sig = signature(stateData);
  if (sig === remote.lastSignature) return;
  remote.lastSignature = sig;
  const target = remote.sessionRef;
  writeChain = writeChain.then(() => updateDoc(target, {
    ...stateData, updatedAt: serverTimestamp()
  })).catch(handleError);
};
function cleanupListeners() {
  for (const unsubscribe of remote.unsubscribers) unsubscribe();
  remote.unsubscribers = [];
}
function controllerUrl(id) {
  const url = new URL(location.href);
  url.hash = "";
  url.search = "";
  url.searchParams.set("sync", "firebase");
  url.searchParams.set("remote", id);
  return url.href;
}
function renderQR(id) {
  const href = controllerUrl(id);
  $("pairLink").value = href;
  $("pairQr").replaceChildren();
  if (typeof QRCode !== "function") {
    $("pairQr").textContent = "ספריית QR לא נטענה; אפשר להעתיק את הקישור.";
    return;
  }
  new QRCode($("pairQr"), {
    text: href, width: 228, height: 228,
    colorDark: "#07101d", colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });
}
function watchSession(ref) {
  remote.unsubscribers.push(onSnapshot(ref, snapshotDoc => {
    if (!snapshotDoc.exists() || snapshotDoc.data().status !== "active") {
      remote.connected = false;
      announce("ההצגה הסתיימה או הוחלפה. סרקו קוד QR חדש.", "error");
      refreshUi();
      return;
    }
    const data = snapshotDoc.data();
    if (data.deck !== DECK_ID) {
      announce("קישור אינו שייך למצגת זו", "error");
      return;
    }
    if (isController) {
      remote.connected = data.approvedUid === remote.user.uid;
      if (remote.connected) {
        announce("📱 מחובר למקרן — אפשר לנווט", "connected");
        applyRemote(data);
      } else {
        announce(data.approvedUid ? "הטלפון אינו מורשה. סרקו QR חדש." : "📱 ממתין לאישור במחשב…", "waiting");
      }
    } else {
      remote.connected = !!data.approvedUid;
      if (remote.connected) {
        announce("📱 טלפון מאושר ומחובר דרך Firebase", "connected");
        applyRemote(data);
      } else if (!remote.pending) {
        announce("📱 ממתין לסריקה ולאישור", "waiting");
      }
    }
    refreshUi();
  }, handleError));
}
function watchJoinRequests(ref) {
  const joinCollection = collection(ref, "joinRequests");
  remote.unsubscribers.push(onSnapshot(joinCollection, snap => {
    const requests = snap.docs.filter(d => d.data().uid === d.id);
    remote.pending = requests.find(d => d.id !== remote.user.uid) || null;
    approveButton.hidden = !remote.pending || remote.connected;
    if (!remote.connected && remote.pending) {
      announce("📱 בקשת חיבור הגיעה — אשרו אותה במחשב", "waiting");
      if (!dialog.open) dialog.showModal();
    }
  }, handleError));
}
async function createPresenterSession() {
  if (initializing) return;
  initializing = true;
  try {
    cleanupListeners();
    remote.pending = null;
    remote.connected = false;
    approveButton.hidden = true;
    announce("📱 מכין סנכרון Firebase…");
    const ref = doc(collection(db, COLLECTION));
    const initial = valueSnapshot();
    await setDoc(ref, {
      hostUid: remote.user.uid,
      approvedUid: "",
      deck: DECK_ID,
      status: "active",
      ...initial,
      createdAt: serverTimestamp(),
      updatedAt: serverTimestamp(),
      expiresAt: Timestamp.fromMillis(Date.now() + 4 * 60 * 60 * 1000)
    });
    remote.sessionRef = ref;
    remote.lastSignature = signature(initial);
    renderQR(ref.id);
    watchSession(ref);
    watchJoinRequests(ref);
    announce("📱 קוד QR מוכן — סרקו בטלפון", "waiting");
  } catch (error) {
    handleError(error);
  } finally {
    initializing = false;
  }
}
async function connectController() {
  if (!/^[a-zA-Z0-9]{16,80}$/.test(sessionId)) {
    announce("קישור ה-QR אינו תקין", "error");
    return;
  }
  const ref = doc(db, COLLECTION, sessionId);
  const snapshotDoc = await getDoc(ref);
  if (!snapshotDoc.exists() || snapshotDoc.data().deck !== DECK_ID ||
      snapshotDoc.data().status !== "active") {
    announce("הקוד פג תוקף או אינו שייך למצגת", "error");
    return;
  }
  remote.sessionRef = ref;
  watchSession(ref);
  if (snapshotDoc.data().approvedUid !== remote.user.uid) {
    const reqRef = doc(collection(ref, "joinRequests"), remote.user.uid);
    const existing = await getDoc(reqRef);
    if (!existing.exists()) await setDoc(reqRef, {
      uid: remote.user.uid, createdAt: serverTimestamp()
    });
    announce("📱 בקשה נשלחה — אשרו את הטלפון במחשב", "waiting");
  }
}
async function approve() {
  if (!remote.pending || !remote.sessionRef || remote.connected) return;
  const request = remote.pending;
  approveButton.disabled = true;
  try {
    await updateDoc(remote.sessionRef, {
      approvedUid: request.id, updatedAt: serverTimestamp()
    });
    await deleteDoc(request.ref);
    remote.pending = null;
    approveButton.hidden = true;
    announce("📱 הטלפון אושר!", "connected");
  } catch (error) {
    handleError(error);
  } finally {
    approveButton.disabled = false;
  }
}
async function resetSession() {
  if (isController || initializing) return;
  if (remote.sessionRef) {
    cleanupListeners();
    try {
      await updateDoc(remote.sessionRef, {status: "closed", updatedAt: serverTimestamp()});
    } catch (error) {
      console.warn("Unable to close old presentation session", error);
    }
  }
  remote.sessionRef = null;
  await createPresenterSession();
}

approveButton.addEventListener("click", approve);
resetButton.addEventListener("click", resetSession);
$("pairClose").addEventListener("click", () => dialog.close());
$("pairCopy").addEventListener("click", async () => {
  if (!$("pairLink").value) return;
  try {
    await navigator.clipboard.writeText($("pairLink").value);
    $("pairCopy").textContent = "✓ הועתק";
  } catch {
    $("pairLink").select();
    $("pairCopy").textContent = "בחרו את הקישור והעתיקו";
  }
});
$("remoteToggle").addEventListener("click", () => {
  if (isController) {
    location.reload();
  } else if (!dialog.open) dialog.showModal();
});
if (isController) {
  $("remoteToggle").textContent = "↻ התחבר שוב";
  dialog.hidden = true;
  announce("📱 מתחבר ל-Firebase…");
} else {
  $("remoteToggle").textContent = "📱 QR / Firebase";
  dialog.showModal();
}
refreshUi();
async function bootstrapPresenter() {
  // A teacher-only Google account prevents anonymous strangers from creating
  // unlimited sessions and consuming the English for Noar project's quota.
  const login = document.createElement("button");
  login.type = "button";
  login.className = "pairAction primary";
  login.textContent = "🔐 התחבר עם Google כמורה";
  document.querySelector("#pairDialog .pairActions")?.prepend(login);
  login.addEventListener("click", async () => {
    login.disabled = true;
    announce("Firebase: מתחבר לחשבון המורה…");
    try {
      const signed = await signInWithPopup(auth, new GoogleAuthProvider());
      if (!signed.user || signed.user.isAnonymous) throw new Error("Teacher Google sign-in required");
      remote.user = signed.user;
      login.hidden = true;
      await createPresenterSession();
    } catch (error) {
      handleError(error);
      login.disabled = false;
      login.hidden = false;
    }
  });
  await auth.authStateReady();
  if (auth.currentUser && !auth.currentUser.isAnonymous) {
    remote.user = auth.currentUser;
    login.hidden = true;
    await createPresenterSession();
  } else {
    announce("🔐 לחצו על התחברות Google כדי להפיק QR מאובטח", "waiting");
  }
}
try {
  if (isController) {
    // Preserve an existing signed-in Google session on the phone, if any.
    await auth.authStateReady();
    remote.user = auth.currentUser || (await signInAnonymously(auth)).user;
    await connectController();
  } else {
    await bootstrapPresenter();
  }
} catch (error) {
  handleError(error);
}
