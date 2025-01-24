function fetchAPIValueToSheet(sheetId, sheetName) {

    const url = "xxx"; // Replace with your API URL

    const options = {
    method: "GET", 
    headers: {
       "Content-Type": "application/json",
    },
  };

  try {
    const response = UrlFetchApp.fetch(url, options);

    const data = parseFloat(response.getContentText()); // the idea here was that the output of the PY script is a string. So in order to use the info in various computations, I needed to convert the input into a float. 

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    sheet.getRange("G21").setValue(data);
  } catch (error) {
   
    Logger.log("Error fetching API value: " + error);
  }
}
