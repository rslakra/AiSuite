const fileInput = document.getElementById("file");
const fileName = document.getElementById("fileName");
const uploadBtn = document.getElementById("uploadBtn");
const uploadNote = document.getElementById("uploadNote");
const messages = document.getElementById("messages");
const empty = document.getElementById("empty");
const question = document.getElementById("question");
const sendBtn = document.getElementById("sendBtn");
const modelPickerBtn = document.getElementById("modelPickerBtn");
const modelPickerValue = document.getElementById("modelPickerValue");
const modelPickerMenu = document.getElementById("modelPickerMenu");

let hasDoc = document.body.dataset.hasDocument === "true";
let selectedModel = "";

if (hasDoc) {
  enableChat();
}

function setModelPickerOpen(open) {
  modelPickerBtn.setAttribute("aria-expanded", open ? "true" : "false");
  modelPickerMenu.hidden = !open;
}

function closeModelPicker() {
  setModelPickerOpen(false);
}

function selectModel(name) {
  selectedModel = name;
  modelPickerValue.textContent = name;
  for (const option of modelPickerMenu.querySelectorAll(".model-picker-option")) {
    option.classList.toggle("is-selected", option.dataset.value === name);
  }
  closeModelPicker();
}

function renderModelPicker(models, defaultModel) {
  modelPickerMenu.innerHTML = "";
  for (const name of models) {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "model-picker-option";
    button.dataset.value = name;
    button.textContent = name;
    button.setAttribute("role", "option");
    button.addEventListener("click", () => selectModel(name));
    item.appendChild(button);
    modelPickerMenu.appendChild(item);
  }

  const base = (n) => n.split(":")[0];
  const match = models.find(
    (n) => n === defaultModel || base(n) === base(defaultModel || ""),
  );
  selectModel(match || models[0]);
  modelPickerBtn.disabled = false;
}

function setModelPickerEmpty(message) {
  selectedModel = "";
  modelPickerValue.textContent = message;
  modelPickerMenu.innerHTML = "";
  modelPickerBtn.disabled = true;
  closeModelPicker();
}

async function loadModels() {
  try {
    const res = await fetch("/api/models");
    const data = await res.json();
    const models = data.models || [];
    if (models.length === 0) {
      setModelPickerEmpty("no models found");
      return;
    }
    renderModelPicker(models, data.default || "");
  } catch (err) {
    setModelPickerEmpty("no models found");
  }
}

modelPickerBtn.addEventListener("click", () => {
  if (modelPickerBtn.disabled) {
    return;
  }
  const isOpen = modelPickerBtn.getAttribute("aria-expanded") === "true";
  setModelPickerOpen(!isOpen);
});

document.addEventListener("click", (event) => {
  if (!event.target.closest("#modelPicker")) {
    closeModelPicker();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeModelPicker();
  }
});

loadModels();

fileInput.addEventListener("change", () => {
  const f = fileInput.files[0];
  fileName.textContent = f ? f.name : "No file chosen";
  uploadBtn.disabled = !f;
  uploadNote.textContent = "";
});

uploadBtn.addEventListener("click", async () => {
  const f = fileInput.files[0];
  if (!f) {
    return;
  }

  const body = new FormData();
  body.append("file", f);

  uploadBtn.disabled = true;
  setNote("Reading, chunking, embedding…", "");

  try {
    const res = await fetch("/upload", { method: "POST", body });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Upload failed.");
    }
    setNote(`Indexed ${data.chunks} chunks from ${data.filename}. Ask away.`, "ok");
    enableChat();
  } catch (err) {
    setNote(err.message, "err");
    uploadBtn.disabled = false;
  }
});

function setNote(text, kind) {
  uploadNote.textContent = text;
  uploadNote.className = "upload-note" + (kind ? " " + kind : "");
}

function enableChat() {
  hasDoc = true;
  question.disabled = false;
  sendBtn.disabled = false;
  if (empty) {
    empty.remove();
  }
}

sendBtn.addEventListener("click", ask);
question.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    ask();
  }
});

async function ask() {
  const q = question.value.trim();
  if (!q || !hasDoc) {
    return;
  }

  addMsg(q, "user");
  question.value = "";
  sendBtn.disabled = true;
  const thinking = addMsg("Searching, please wait...", "bot thinking");

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, model: selectedModel }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Something went wrong.");
    }
    thinking.textContent = data.answer;
    thinking.className = "msg bot";
  } catch (err) {
    thinking.textContent = err.message;
    thinking.className = "msg bot";
  } finally {
    sendBtn.disabled = false;
    question.focus();
  }
}

function addMsg(text, cls) {
  const el = document.createElement("div");
  el.className = "msg " + cls;
  el.textContent = text;
  messages.appendChild(el);
  el.scrollIntoView({ behavior: "smooth", block: "end" });
  return el;
}
