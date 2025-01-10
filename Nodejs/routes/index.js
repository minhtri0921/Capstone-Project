const dataRouter = require("./data");

function route(app) {
  app.use("/api/v1", dataRouter);
}

module.exports = route;
