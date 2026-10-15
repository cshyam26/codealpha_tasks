
const source = document.getElementById("source");
const target = document.getElementById("target");
const inputText = document.getElementById("inputText");
const outputText = document.getElementById("outputText");
const translateBtn = document.getElementById("translate");
const status = document.getElementById("status");
const counter = document.getElementById("counter");

let translatedText = "";

inputText.addEventListener("input", () => {
  counter.textContent = `${inputText.value.length} / 500`;
});

document.getElementById("clear").addEventListener("click", () => {
  inputText.value = "";
  translatedText = "";
  outputText.textContent = "Your translation will appear here...";
  counter.textContent = "0 / 500";
  status.textContent = "";
});

document.getElementById("swap").addEventListener("click", () => {
  const previousSource = source.value;
  source.value = target.value;
  target.value = previousSource;

  translatedText = "";
  outputText.textContent = "Your translation will appear here...";
  status.textContent = "Languages swapped.";
});

translateBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();

  if (!text) {
    status.textContent = "Please enter some text first.";
    return;
  }

  translateBtn.disabled = true;
  translateBtn.textContent = "Translating...";
  status.textContent = "Please wait...";
  translatedText = "";

  try {
    const response = await fetch("/api/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        source: source.value,
        target: target.value
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Translation failed.");
    }

    translatedText = data.translatedText;
    outputText.textContent = translatedText;
    status.textContent = "Translation completed successfully.";
  } catch (error) {
    outputText.textContent = "Translation unavailable.";
    status.textContent = error.message || "Please try again later.";
  } finally {
    translateBtn.disabled = false;
    translateBtn.innerHTML = 'Translate now <span>→</span>';
  }
});

document.getElementById("copy").addEventListener("click", async () => {
  if (!translatedText) {
    status.textContent = "Translate some text before copying.";
    return;
  }

  try {
    await navigator.clipboard.writeText(translatedText);
    status.textContent = "Copied successfully!";
  } catch {
    status.textContent = "Copy failed. Please copy the text manually.";
  }
});

document.getElementById("speak").addEventListener("click", () => {
  if (!translatedText) {
    status.textContent = "Translate some text before listening.";
    return;
  }

  if (!("speechSynthesis" in window)) {
    status.textContent = "Speech is not supported in this browser.";
    return;
  }

  window.speechSynthesis.cancel();

  const speech = new SpeechSynthesisUtterance(translatedText);
  speech.lang = target.value;
  window.speechSynthesis.speak(speech);
});
