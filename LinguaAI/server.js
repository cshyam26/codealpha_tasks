
const express = require("express");
const path = require("path");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json({ limit: "20kb" }));
app.use(express.static(path.join(__dirname, "public")));

const supportedLanguages = [
  "en", "te", "hi", "ta", "kn", "ml",
  "fr", "es", "de", "it", "ja", "ko",
  "zh", "ar", "pt", "ru", "bn", "mr"
];

app.post("/api/translate", async (req, res) => {
  try {
    const { text, source, target } = req.body;

    if (
      typeof text !== "string" ||
      typeof source !== "string" ||
      typeof target !== "string"
    ) {
      return res.status(400).json({
        error: "Please provide text and select both languages."
      });
    }

    const input = text.trim();

    if (!input) {
      return res.status(400).json({
        error: "Please enter text to translate."
      });
    }

    if (input.length > 500) {
      return res.status(400).json({
        error: "Text must be 500 characters or fewer."
      });
    }

    if (
      !supportedLanguages.includes(source) ||
      !supportedLanguages.includes(target)
    ) {
      return res.status(400).json({
        error: "Unsupported language selection."
      });
    }

    if (source === target) {
      return res.json({
        translatedText: input,
        source,
        target
      });
    }

    let translatedText = "";

    // Try the publicly accessible Google Translate endpoint first.
    try {
      const googleParams = new URLSearchParams({
        client: "gtx",
        sl: source,
        tl: target,
        dt: "t",
        q: input
      });

      const googleResponse = await fetch(
        `https://translate.googleapis.com/translate_a/single?${googleParams}`,
        { signal: AbortSignal.timeout(10000) }
      );

      if (googleResponse.ok) {
        const googleData = await googleResponse.json();

        if (Array.isArray(googleData?.[0])) {
          translatedText = googleData[0]
            .map(part => Array.isArray(part) ? part[0] || "" : "")
            .join("")
            .trim();
        }
      }
    } catch (error) {
      console.log("Primary translation service unavailable.");
    }

    // If the first service fails, try MyMemory.
    if (!translatedText) {
      try {
        const memoryParams = new URLSearchParams({
          q: input,
          langpair: `${source}|${target}`
        });

        const memoryResponse = await fetch(
          `https://api.mymemory.translated.net/get?${memoryParams}`,
          { signal: AbortSignal.timeout(10000) }
        );

        if (memoryResponse.ok) {
          const memoryData = await memoryResponse.json();

          if (
            memoryData.responseStatus === 200 &&
            memoryData.responseData?.translatedText
          ) {
            translatedText =
              memoryData.responseData.translatedText.trim();
          }
        }
      } catch (error) {
        console.log("Fallback translation service unavailable.");
      }
    }

    if (!translatedText) {
      return res.status(502).json({
        error: "Translation services are unavailable. Please try again."
      });
    }
    return res.json({
      translatedText,
      source,
      target
    });

  } catch (error) {
    console.error("Translation error:", error.message);

    return res.status(502).json({
      error: "Translation service unavailable. Check your internet connection."
    });
  }
});

app.listen(PORT, () => {
  console.log(`LinguaAI running at http://localhost:${PORT}`);
});
