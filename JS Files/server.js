const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const port = 3000;

let users = [];

app.use(bodyParser.json());
app.use(express.static(__dirname));

app.post("/api/create-account", (req, res) => {
  const { username, password } = req.body;

  if (users.find((user) => user.username === username)) {
    return res.json({ success: false, message: "Username already exists." });
  }

  users.push({ username, password });
  res.json({ success: true });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
