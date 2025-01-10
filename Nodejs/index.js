const express = require("express");
const cors = require("cors");
const app = express();

app.use(express.json());

app.use(cors());

const route = require("./routes");

app.use(express.static(__dirname + "/client"));

// Router init
route(app);

// app.get("/", function (req, res) {
//   res.sendFile(__dirname + "/client/index.html");
// });

// Start server
const port = 3001;
app.listen(port, () => console.log(`Server is starting on port ${port}`));
