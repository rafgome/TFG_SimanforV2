const XLSX = require("xlsx");
const SHEET1_LENGTH = 13;
const SHEET2_LENGTH = 42;

function validateXlsx(workbook){
  const header1 = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1 }).shift();
  const header2 = XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[1]], { header: 1 }).shift();
  if (!header1 | !header2){
    return false;
  }
  return header1.length == SHEET1_LENGTH & header2.length == SHEET2_LENGTH;
}

function validateCsv(data1, data2){
  const header1 = data1[0];
  const header2 = data2[0];
  if (!header1 | !header2){
    return false;
  }
  return Object.keys(header1).length == SHEET1_LENGTH & Object.keys(header2).length == SHEET2_LENGTH;
}

function parseCsv(file){
  let lines = file.split("\n");
  let headers = lines[0].split(",");
  let result = [];
  for (let i = 1; i < lines.length; i++) {
    let obj = [];
    let currentline = lines[i].split(",");
    for (let j = 0; j < headers.length; j++) {
      if (currentline[j] === undefined){
        continue;
      }
      obj.push(currentline[j].replace(/"/g, ""));
    }
    result.push(obj);
  }
  return result;
}

module.exports = {
  validateXlsx,
  validateCsv,
  parseCsv
};
