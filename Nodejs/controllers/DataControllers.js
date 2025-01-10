const xlsx = require("xlsx");
const path = require("path");

const filePath = path.join(
  "C:",
  "MinhTri",
  "DATN_2024",
  "data_job",
  "job_data.xlsx"
);

class DataControllers {
  async getData(req, res) {
    try {
      // Đọc file Excel
      const workbook = xlsx.readFile(filePath);

      // Lấy sheet từ file Excel (giả sử sheet tên là 'job_data')
      const sheet = workbook.Sheets["job_data"];

      // Chuyển dữ liệu từ sheet thành dạng JSON
      const data = xlsx.utils.sheet_to_json(sheet);

      // Trả về dữ liệu dưới dạng JSON
      console.log("123");
      res.status(200).json(data);
    } catch (err) {
      console.log(err);

      // Nếu có lỗi, trả về mã lỗi 500 và thông báo lỗi
      res.status(500).json({ error: "Error reading Excel file", details: err });
    }
  }

  async postData(req, res) {
    try {
      // Lấy dữ liệu từ body của request
      const {
        Title,
        Company_Name,
        Place,
        Number_Employee,
        job_title,
        Level,
        Salary,
        Education,
        Description,
        Requirement,
        Deadline,
        Source_Picture,
      } = req.body;

      // Kiểm tra dữ liệu có đầy đủ không
      if (
        !Title ||
        !Company_Name ||
        !Place ||
        !Number_Employee ||
        !job_title ||
        !Level ||
        !Salary ||
        !Education ||
        !Description ||
        !Requirement ||
        !Deadline ||
        !Source_Picture
      ) {
        return res.status(400).json({ error: "All fields are required" });
      }

      // Đọc file Excel
      const workbook = xlsx.readFile(filePath);

      // Lấy sheet từ file Excel (giả sử sheet tên là 'job_data')
      const sheet = workbook.Sheets["job_data"];

      // Chuyển dữ liệu từ sheet thành JSON
      const data = xlsx.utils.sheet_to_json(sheet);

      // Tìm Id lớn nhất hiện tại
      const maxId = data.reduce(
        (max, item) => (item.Id > max ? item.Id : max),
        0
      );

      // Tạo Id mới
      const newId = maxId + 1;

      // Thêm dữ liệu mới với Id
      const newData = {
        Id: newId,
        Title,
        Company_Name,
        Place,
        Number_Employee,
        job_title,
        Level,
        Salary,
        Education,
        Description,
        Requirement,
        Deadline,
        Source_Picture,
      };
      data.push(newData);

      // Chuyển mảng JSON trở lại thành sheet
      const newSheet = xlsx.utils.json_to_sheet(data);

      // Ghi sheet mới trở lại file Excel
      workbook.Sheets["job_data"] = newSheet;
      xlsx.writeFile(workbook, filePath);

      // Trả về phản hồi thành công
      res
        .status(200)
        .json({ message: "Data added successfully", data: newData });
    } catch (err) {
      // Nếu có lỗi, trả về mã lỗi 500 và thông báo lỗi
      console.log(err);
      res
        .status(500)
        .json({ error: "Error writing to Excel file", details: err });
    }
  }

  async editData(req, res) {}

  async deleteDataById(req, res) {
    try {
      const id = parseInt(req.params.id); // Lấy id từ params và chuyển thành số nguyên
      console.log(id);

      if (isNaN(id)) {
        return res.status(400).json({ error: "Invalid ID" });
      }

      // Đọc file Excel
      const workbook = xlsx.readFile(filePath);
      const sheet = workbook.Sheets["job_data"];
      const data = xlsx.utils.sheet_to_json(sheet);

      // Kiểm tra xem Id có tồn tại không
      const index = data.findIndex((item) => item.Id === id);

      if (index === -1) {
        return res.status(404).json({ error: "ID not found" });
      }

      // Xóa phần tử tại vị trí `index`
      data.splice(index, 1);

      // Cập nhật lại các Id để duy trì tính liên tục
      const updatedData = data.map((item, idx) => ({
        ...item,
        Id: idx + 1, // Gán lại Id liên tục, bắt đầu từ 1
      }));

      // Chuyển lại dữ liệu JSON thành sheet
      const newSheet = xlsx.utils.json_to_sheet(updatedData, {
        header: [
          "Id",
          "Title",
          "Company_Name",
          "Place",
          "Number_Employee",
          "job_title",
          "Level",
          "Salary",
          "Education",
          "Description",
          "Requirement",
          "Deadline",
          "Source_Picture",
        ],
      });

      // Cập nhật sheet trong workbook
      workbook.Sheets["job_data"] = newSheet;

      // Ghi lại file Excel
      xlsx.writeFile(workbook, filePath);

      res.status(200).json({
        message: `Data with ID ${id} deleted successfully`,
        data: updatedData,
      });
    } catch (err) {
      console.error(err);
      res.status(500).json({ error: "Error deleting data", details: err });
    }
  }
}

module.exports = new DataControllers();
