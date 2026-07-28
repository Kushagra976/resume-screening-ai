const apiStatus = document.querySelector("#api-status");
const indexedCount = document.querySelector("#indexed-count");
const modelName = document.querySelector("#model-name");
const embeddingDimension = document.querySelector("#embedding-dimension");
const fileInput = document.querySelector("#resume-file");
const fileSummary = document.querySelector("#file-summary");
const uploadForm = document.querySelector("#upload-form");
const uploadList = document.querySelector("#upload-list");
const rankForm = document.querySelector("#rank-form");
const results = document.querySelector("#results");
const resultsSummary = document.querySelector("#results-summary");
const resultTemplate = document.querySelector("#result-template");
const API_BASE =
  window.location.origin === "null" ||
  !["127.0.0.1:8000", "localhost:8000"].includes(window.location.host)
    ? "http://127.0.0.1:8000"
    : "";

function setStatus(text, state) {
  apiStatus.textContent = text;
  apiStatus.className = `status-pill ${state || ""}`.trim();
}

async function requestJson(url, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE}${url}`, options);
  } catch (error) {
    throw new Error(
      "Cannot reach the API. Start FastAPI and open http://127.0.0.1:8000/app/."
    );
  }

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const detail = payload?.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join(", ")
      : detail || `Request failed with ${response.status}`;
    throw new Error(message);
  }

  return payload;
}

async function refreshStats() {
  try {
    const stats = await requestJson("/stats");
    indexedCount.textContent = stats.indexed_resume_count;
    modelName.textContent = stats.model_name;
    embeddingDimension.textContent = stats.embedding_dimension;
    setStatus("API ready", "ok");
  } catch (error) {
    setStatus("API unavailable", "error");
    modelName.textContent = "Unavailable";
    embeddingDimension.textContent = "-";
  }
}

function updateFileSummary() {
  const files = [...fileInput.files];

  if (files.length === 0) {
    fileSummary.textContent = "No files selected";
    return;
  }

  fileSummary.textContent =
    files.length === 1 ? files[0].name : `${files.length} files selected`;
}

function appendUploadMessage(text, state) {
  const item = document.createElement("li");
  item.textContent = text;
  item.className = state;
  uploadList.prepend(item);
}

async function uploadResume(file) {
  const formData = new FormData();
  formData.append("file", file);

  return requestJson("/resume", {
    method: "POST",
    body: formData,
  });
}

async function handleUpload(event) {
  event.preventDefault();

  const files = [...fileInput.files];
  if (files.length === 0) {
    appendUploadMessage("Choose at least one PDF before uploading.", "error");
    return;
  }

  const button = uploadForm.querySelector("button");
  button.disabled = true;
  button.textContent = "Indexing...";

  for (const file of files) {
    try {
      const response = await uploadResume(file);
      appendUploadMessage(`${file.name} indexed as resume #${response.resume_id}.`, "success");
    } catch (error) {
      appendUploadMessage(`${file.name}: ${error.message}`, "error");
    }
  }

  fileInput.value = "";
  updateFileSummary();
  button.disabled = false;
  button.textContent = "Upload and index";
  await refreshStats();
}

function renderEmptyResults(message) {
  results.innerHTML = "";
  const empty = document.createElement("p");
  empty.className = "empty-state";
  empty.textContent = message;
  results.append(empty);
}

function resumeName(path) {
  return path.split(/[\\/]/).pop()?.replace(/^[a-f0-9]{32}_/, "") || "Resume";
}

function renderResults(matches) {
  results.innerHTML = "";

  if (matches.length === 0) {
    renderEmptyResults("No matches returned. Add resumes first, then try again.");
    return;
  }

  for (const match of matches) {
    const node = resultTemplate.content.firstElementChild.cloneNode(true);
    const metadata = match.metadata;

    node.querySelector(".score-value").textContent = `${Math.round(match.score * 100)}%`;
    node.querySelector("h3").textContent = resumeName(metadata.resume_path);
    node.querySelector('[data-field="email"]').textContent = metadata.email || "Not found";
    node.querySelector('[data-field="phone"]').textContent = metadata.phone || "Not found";
    node.querySelector('[data-field="github"]').textContent = metadata.github || "Not found";
    node.querySelector('[data-field="linkedin"]').textContent = metadata.linkedin || "Not found";

    results.append(node);
  }
}

async function handleRank(event) {
  event.preventDefault();

  const formData = new FormData(rankForm);
  const jobDescription = formData.get("job-description").trim();
  const topK = Number(formData.get("top-k")) || 5;
  const button = rankForm.querySelector("button");

  if (!jobDescription) {
    renderEmptyResults("Paste a job description before ranking.");
    return;
  }

  button.disabled = true;
  button.textContent = "Ranking...";
  resultsSummary.textContent = "Scoring resumes against the job description.";

  try {
    const response = await requestJson("/rank", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        job_description: jobDescription,
        top_k: topK,
      }),
    });

    resultsSummary.textContent = `${response.matches.length} match${
      response.matches.length === 1 ? "" : "es"
    } returned.`;
    renderResults(response.matches);
  } catch (error) {
    resultsSummary.textContent = "Ranking failed.";
    renderEmptyResults(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Rank resumes";
  }
}

fileInput.addEventListener("change", updateFileSummary);
uploadForm.addEventListener("submit", handleUpload);
rankForm.addEventListener("submit", handleRank);

renderEmptyResults("Upload resumes, then run a match.");
refreshStats();
