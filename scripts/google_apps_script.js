/**
 * Solarian Waitlist — Google Apps Script
 *
 * 部署步骤：
 * 1. 打开 https://sheets.new 新建表格，命名为 "Solarian Waitlist"
 * 2. 第一行写表头：timestamp | name | email | country | industry | role | painpoints | usecase
 * 3. 点 Extensions → Apps Script
 * 4. 删掉默认代码，粘贴本文件全部内容
 * 5. 点 Deploy → New deployment
 * 6. 类型选 "Web app"
 * 7. Execute as: Me, Who has access: Anyone
 * 8. 点 Deploy，复制生成的 URL
 * 9. 把 URL 粘贴到 index.html 中的 WAITLIST_ENDPOINT 变量
 */

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date().toISOString(),
    data.name || '',
    data.email || '',
    data.country || '',
    data.industry || '',
    data.role || '',
    data.painpoints || '',
    data.usecase || ''
  ]);

  // Send notification email
  try {
    MailApp.sendEmail(
      'jinhanchen0427@gmail.com',
      'New Solarian Waitlist Signup: ' + (data.name || 'Unknown'),
      'Name: ' + data.name + '\n' +
      'Email: ' + data.email + '\n' +
      'Country: ' + data.country + '\n' +
      'Industry: ' + data.industry + '\n' +
      'Role: ' + (data.role || 'N/A') + '\n' +
      'Pain Points: ' + (data.painpoints || 'N/A') + '\n' +
      'Use Case: ' + (data.usecase || 'N/A')
    );
  } catch(err) {}

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'Solarian Waitlist API is running' }))
    .setMimeType(ContentService.MimeType.JSON);
}
