// server.js (CommonJS)
const express = require("express");
const fetch = require("node-fetch"); // node-fetch v3 exports only ESM by default; use v2 or a workaround
const morgan = require("morgan");
const bodyParser = require("body-parser");
const path = require("path");

// If node-fetch v3 causes trouble with require(), install v2:
// npm install node-fetch@2
// and then use: const fetch = require("node-fetch");

const app = express();
app.use(morgan("dev"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve static files
app.use(express.static(path.join(__dirname, "public")));

// Proxy endpoint
app.post("/api/submit", async (req, res) => {
  try {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:5000/api/submit";

    const backendRes = await fetch(backendUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body),
    });

    let data = {};
    try { data = await backendRes.json(); } catch (e) {}

    res.status(backendRes.status).json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Backend unreachable", details: String(err) });
  }
});

app.get("/health", (req, res) => res.json({ status: "ok" }));

app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "templates", "index.html"));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Frontend running on port ${PORT}`));
