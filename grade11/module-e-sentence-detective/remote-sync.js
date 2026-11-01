/*
 * Module E Sentence Detective — isolated phone remote for Grade 11.
 * PeerJS Cloud provides signaling; slide data travels over a WebRTC data channel.
 * The temporary, hard-to-guess peer ID in the QR URL acts as the pairing token.
 * No presentation answers or student identities are saved on a server.
 */
(() => {
  "use strict";
  const remoteId = new URLSearchParams(location.search).get("remote");
  const isController = !!remoteId;
  const remote = {
    role: isController ? "controller" : "presenter",
    connected: false,
    applying: false,
    peer: null,
    connection: null,
    clients: new Set(),
    pending: null,
    authorizedPeerId: null,
    retryTimer: null,
    lastSyncedState: null
  };
  window.deckRemote = remote;
  document.body.classList.add(isController ? "remote-controller" : "remote-presenter");
  const statusButton = document.getElementById("remoteToggle");
  const syncBadge = document.getElementById("syncBadge");
  const dialog = document.getElementById("pairDialog");
  const statusText = document.getElementById("pairStatus");
  const qrTarget = document.getElementById("pairQr");
  const linkField = document.getElementById("pairLink");
  const copyButton = document.getElementById("pairCopy");
  const closeButton = document.getElementById("pairClose");
  const approveButton = document.getElementById("pairApprove");
  const resetButton = document.getElementById("pairReset");

  function announce(message, tone) {
    syncBadge.textContent = message;
    syncBadge.dataset.tone = tone || "waiting";
    if (!isController) statusText.textContent = message;
  }
  function snapshot() {
    return {
      type: "state",
      index: state.index,
      stage: state.stage,
      selected: Object.assign({}, state.selected)
    };
  }
  function sanitize(message) {
    if (!message || message.type !== "state"
        || !Number.isInteger(message.index) || message.index < 0 || message.index >= slides.length
        || !Number.isInteger(message.stage) || message.stage < 0 || message.stage > 4
        || !message.selected || typeof message.selected !== "object"
        || Array.isArray(message.selected)) return null;
    const chosen = {};
    Object.entries(message.selected).forEach(([key, value]) => {
      const i = Number(key);
      if (Number.isInteger(i) && i >= 0 && i < slides.length
          && Number.isInteger(value) && value >= 0
          && value < (slides[i].choices || []).length) chosen[i] = value;
    });
    return { index: message.index, stage: message.stage, selected: chosen };
  }
  function applySnapshot(message) {
    const update = sanitize(message);
    if (!update) return false;
    remote.applying = true;
    try {
      state.index = update.index;
      state.stage = update.stage;
      state.selected = update.selected;
      remote.lastSyncedState = update;
      render();
    } finally {
      remote.applying = false;
    }
    return true;
  }
  function uiConnectionState() {
    if (!isController) return;
    document.getElementById("prev").disabled = !remote.connected || state.index === 0;
    document.getElementById("next").disabled = !remote.connected || state.index === slides.length - 1;
    document.getElementById("reveal").disabled = !remote.connected;
    document.getElementById("reset").disabled = !remote.connected || (
      state.stage === 0 && state.selected[state.index] === undefined
    );
    document.querySelectorAll("[data-choice]").forEach(btn => { btn.disabled = !remote.connected; });
  }
  remote.canNavigate = () => !isController || remote.connected;
  remote.syncUi = uiConnectionState;
  remote.broadcast = () => {
    if (remote.applying) return;
    const message = snapshot();
    if (isController) {
      if (remote.connected && remote.connection && remote.connection.open) {
        remote.connection.send(message);
      }
    } else {
      remote.clients.forEach(connection => {
        if (connection.open) connection.send(message);
      });
    }
    uiConnectionState();
  };
  function updatePresenterCount() {
    const count = [...remote.clients].filter(conn => conn.open).length;
    approveButton.hidden = !(remote.pending && remote.pending.open);
    if (count) announce("📱 הטלפון אושר ומחובר", "connected");
    else if (remote.pending && remote.pending.open) announce("📱 טלפון ממתין לאישור — לחצו על אישור", "waiting");
    else if (remote.authorizedPeerId) announce("📱 הטלפון נותק — התחברו שוב או אפסו חיבור", "waiting");
    else announce("📱 ממתין לסריקה", "waiting");
  }
  function pairedUrl(peerId) {
    const url = new URL(location.href);
    url.hash = "";
    url.search = "";
    url.searchParams.set("sync", "peer");
    url.searchParams.set("remote", peerId);
    return url.href;
  }
  function displayQR(peerId) {
    const url = pairedUrl(peerId);
    linkField.value = url;
    qrTarget.replaceChildren();
    if (typeof QRCode === "function") {
      new QRCode(qrTarget, {
        text: url,
        width: 228,
        height: 228,
        colorDark: "#07101d",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.M
      });
    } else {
      qrTarget.textContent = "לא ניתן להציג QR. אפשר להעתיק את הקישור שמתחתיו.";
    }
  }
  function setControllerStatus(connected, message, tone) {
    remote.connected = connected;
    announce(message, tone);
    uiConnectionState();
  }
  function reconnectLater() {
    if (remote.retryTimer) return;
    remote.retryTimer = setTimeout(() => {
      remote.retryTimer = null;
      if (!remote.connected && remote.peer && !remote.peer.destroyed && !remote.peer.disconnected) connectController();
    }, 4500);
  }
  function connectController() {
    if (!remote.peer || remote.peer.destroyed || remote.peer.disconnected) return;
    setControllerStatus(false, "📱 מתחבר למקרן…", "waiting");
    const connection = remote.peer.connect(remoteId, { serialization: "json" });
    remote.connection = connection;
    let opened = false;
    const watchdog = setTimeout(() => {
      if (!opened && remote.connection === connection) {
        connection.close();
        setControllerStatus(false, "לא הצלחנו להתחבר — מנסים שוב", "error");
        reconnectLater();
      }
    }, 12000);
    let denied = false;
    connection.on("open", () => {
      clearTimeout(watchdog);
      if (remote.connection !== connection) return;
      opened = true;
      setControllerStatus(false, "📱 ממתין לאישור החיבור במחשב…", "waiting");
      connection.send({ type: "hello" });
    });
    connection.on("data", message => {
      if (remote.connection !== connection || !message) return;
      if (message.type === "approved") {
        setControllerStatus(true, "📱 מחובר למקרן — אפשר לנווט", "connected");
      } else if (message.type === "state" && remote.connected) {
        applySnapshot(message);
      } else if (["denied", "busy", "unpaired"].includes(message.type)) {
        denied = true;
        setControllerStatus(false, "📱 חיבור נדחה — בקשו אישור או איפוס במחשב", "error");
        connection.close();
      }
    });
    const lost = () => {
      clearTimeout(watchdog);
      if (remote.connection !== connection) return;
      setControllerStatus(false, denied ? "📱 נדרש אישור חדש במחשב" : "📱 החיבור נותק — מתחבר מחדש…", "error");
      if (!denied) reconnectLater();
    };
    connection.on("close", lost);
    connection.on("error", lost);
  }
  function connectPresenter() {
    announce("מכין קוד QR…", "waiting");
    remote.peer = new Peer();
    remote.peer.on("open", id => {
      displayQR(id);
      updatePresenterCount();
    });
    remote.peer.on("connection", connection => {
      connection.on("open", () => {
        if (remote.authorizedPeerId && connection.peer !== remote.authorizedPeerId) {
          connection.send({ type: "denied" });
          setTimeout(() => connection.close(), 400);
        } else if (remote.authorizedPeerId === connection.peer) {
          remote.clients.add(connection);
          connection.send({ type: "approved" });
          connection.send(snapshot());
        } else if (!remote.pending) {
          remote.pending = connection;
        } else {
          connection.send({ type: "busy" });
          setTimeout(() => connection.close(), 400);
        }
        updatePresenterCount();
      });
      connection.on("data", message => {
        if (!remote.clients.has(connection) || !connection.open || !message || typeof message !== "object") return;
        if (message.type === "hello") connection.send(snapshot());
        else if (message.type === "state" && applySnapshot(message)) {
          // Only an explicitly approved phone can alter the projected slides.
          remote.broadcast();
        }
      });
      const lost = () => {
        remote.clients.delete(connection);
        if (remote.pending === connection) remote.pending = null;
        updatePresenterCount();
      };
      connection.on("close", lost);
      connection.on("error", lost);
    });
    remote.peer.on("error", error => {
      announce("שגיאת חיבור: " + (error.type || "לא ניתן להתחבר"), "error");
    });
    remote.peer.on("disconnected", () => {
      if (!remote.peer.destroyed) remote.peer.reconnect();
    });
  }
  function startController() {
    if (!/^[A-Za-z0-9_-]{6,128}$/.test(remoteId)) {
      setControllerStatus(false, "קישור QR לא תקין", "error");
      return;
    }
    setControllerStatus(false, "📱 מתחבר למקרן…", "waiting");
    remote.peer = new Peer();
    remote.peer.on("open", connectController);
    remote.peer.on("disconnected", () => {
      setControllerStatus(false, "📱 חיבור האינטרנט נותק", "error");
      if (!remote.peer.destroyed) remote.peer.reconnect();
    });
    remote.peer.on("error", error => {
      setControllerStatus(false, "📱 בעיית חיבור (" + (error.type || "שגיאה") + ")", "error");
      reconnectLater();
    });
  }
  approveButton.addEventListener("click", () => {
    const connection = remote.pending;
    if (!connection || !connection.open) return;
    remote.pending = null;
    remote.authorizedPeerId = connection.peer;
    remote.clients.add(connection);
    connection.send({ type: "approved" });
    connection.send(snapshot());
    updatePresenterCount();
  });
  resetButton.addEventListener("click", () => {
    remote.clients.forEach(connection => {
      if (connection.open) connection.send({ type: "unpaired" });
      connection.close();
    });
    remote.clients.clear();
    if (remote.pending) remote.pending.close();
    remote.pending = null;
    remote.authorizedPeerId = null;
    updatePresenterCount();
  });
  copyButton.addEventListener("click", async () => {
    if (!linkField.value) return;
    try {
      await navigator.clipboard.writeText(linkField.value);
      copyButton.textContent = "✓ הועתק";
    } catch (_) {
      linkField.select();
      copyButton.textContent = "בחר את הקישור והעתק";
    }
  });
  closeButton.addEventListener("click", () => dialog.close());
  statusButton.addEventListener("click", () => {
    if (isController) { location.reload(); return; }
    if (!dialog.open) dialog.showModal();
  });
  if (isController) {
    statusButton.textContent = "↻ התחבר שוב";
    statusButton.title = "רענון חיבור השלט";
    dialog.hidden = true;
  } else {
    statusButton.textContent = "📱 QR / שלט";
    dialog.showModal();
  }
  if (typeof Peer !== "function") {
    announce("ספריית החיבור לא נטענה — אפשר להמשיך ללא שלט", "error");
    uiConnectionState();
    return;
  }
  if (isController) startController();
  else connectPresenter();
})();