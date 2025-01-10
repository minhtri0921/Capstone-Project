const express = require("express");
const router = express.Router();

const DataControllers = require("../controllers/DataControllers");

router.get("/", DataControllers.getData);
router.post("/addData", DataControllers.postData);
// router.put("/", DataControllers.editData);
router.delete("/delete/:id", DataControllers.deleteDataById);

module.exports = router;
