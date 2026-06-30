// ConversationQA - Meeting Notes & Q&A Application
// Google Apps Script Implementation

const SHEET_NAMES = {
  MEETINGS: 'Meetings',
  CONVERSATIONS: 'Conversations',
  USERS: 'Users',
  SETTINGS: 'Settings'
};

// Initialize sheets if they don't exist
function initializeSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // Create Meetings sheet
  if (!ss.getSheetByName(SHEET_NAMES.MEETINGS)) {
    const meetingSheet = ss.insertSheet(SHEET_NAMES.MEETINGS);
    meetingSheet.appendRow(['ID', 'Title', 'Date', 'Description', 'Participants', 'Notes', 'Created By', 'Created At', 'Updated At', 'Status']);
    meetingSheet.getRange(1, 1, 1, 10).setFontWeight('bold').setBackground('#4472C4').setFontColor('#FFFFFF');
  }

  // Create Conversations sheet
  if (!ss.getSheetByName(SHEET_NAMES.CONVERSATIONS)) {
    const convSheet = ss.insertSheet(SHEET_NAMES.CONVERSATIONS);
    convSheet.appendRow(['ID', 'Meeting ID', 'Type', 'Author', 'Content', 'Timestamp', 'Likes', 'Status']);
    convSheet.getRange(1, 1, 1, 8).setFontWeight('bold').setBackground('#70AD47').setFontColor('#FFFFFF');
  }

  // Create Users sheet
  if (!ss.getSheetByName(SHEET_NAMES.USERS)) {
    const userSheet = ss.insertSheet(SHEET_NAMES.USERS);
    userSheet.appendRow(['Email', 'Name', 'Department', 'Joined Date', 'Status']);
    userSheet.getRange(1, 1, 1, 5).setFontWeight('bold').setBackground('#FFC000').setFontColor('#000000');
  }
}

// doGet - Main entry point for the web app
function doGet(e) {
  Logger.log('User: ' + Session.getActiveUser().getEmail());

  const userEmail = Session.getActiveUser().getEmail();
  if (!userEmail) {
    return HtmlService.createHtmlOutput('Please log in with your Google account.');
  }

  // Initialize sheets on first load
  initializeSheets();

  // Register user if new
  registerUserIfNew(userEmail);

  const html = HtmlService.createTemplateFromFile('index');
  html.userEmail = userEmail;
  html.userName = getUserName(userEmail);

  return html.evaluate()
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Register user if they're new to the system
function registerUserIfNew(email) {
  const userSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAMES.USERS);
  const data = userSheet.getRange(2, 1, userSheet.getLastRow() - 1, 5).getValues();

  const existingUser = data.find(row => row[0] === email);
  if (!existingUser) {
    const user = Session.getActiveUser();
    userSheet.appendRow([email, user.getName() || 'Unknown', '', new Date(), 'Active']);
  }
}

// Get user's display name
function getUserName(email) {
  const userSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAMES.USERS);
  const data = userSheet.getRange(2, 1, userSheet.getLastRow() - 1, 5).getValues();

  const user = data.find(row => row[0] === email);
  return user ? user[1] : 'Unknown User';
}

// Create a new meeting
function createMeeting(title, description, participants) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const meetingSheet = ss.getSheetByName(SHEET_NAMES.MEETINGS);

  const id = 'MTG_' + Date.now();
  const now = new Date();

  meetingSheet.appendRow([
    id,
    title,
    Utilities.formatDate(now, Session.getScriptTimeZone(), 'yyyy-MM-dd'),
    description,
    participants,
    '',
    Session.getActiveUser().getEmail(),
    now,
    now,
    'Active'
  ]);

  return id;
}

// Get all meetings for user
function getMeetings() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const meetingSheet = ss.getSheetByName(SHEET_NAMES.MEETINGS);
  const data = meetingSheet.getRange(2, 1, meetingSheet.getLastRow() - 1, 10).getValues();

  return data.map(row => ({
    id: row[0],
    title: row[1],
    date: row[2],
    description: row[3],
    participants: row[4],
    notes: row[5],
    createdBy: row[6],
    createdAt: row[7],
    updatedAt: row[8],
    status: row[9]
  }));
}

// Get meetings by ID
function getMeetingById(meetingId) {
  const meetings = getMeetings();
  return meetings.find(m => m.id === meetingId);
}

// Add conversation (question/note/comment)
function addConversation(meetingId, type, content) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const convSheet = ss.getSheetByName(SHEET_NAMES.CONVERSATIONS);

  const id = 'CONV_' + Date.now();
  const now = new Date();
  const author = getUserName(Session.getActiveUser().getEmail());

  convSheet.appendRow([
    id,
    meetingId,
    type, // 'note', 'question', 'comment'
    author,
    content,
    now,
    0, // likes
    'Active'
  ]);

  return id;
}

// Get conversations for a meeting
function getConversationsByMeetingId(meetingId) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const convSheet = ss.getSheetByName(SHEET_NAMES.CONVERSATIONS);
  const data = convSheet.getRange(2, 1, convSheet.getLastRow() - 1, 8).getValues();

  return data
    .filter(row => row[1] === meetingId)
    .map(row => ({
      id: row[0],
      meetingId: row[1],
      type: row[2],
      author: row[3],
      content: row[4],
      timestamp: row[5],
      likes: row[6],
      status: row[7]
    }))
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
}

// Update meeting notes
function updateMeetingNotes(meetingId, notes) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const meetingSheet = ss.getSheetByName(SHEET_NAMES.MEETINGS);
  const data = meetingSheet.getRange(2, 1, meetingSheet.getLastRow() - 1, 10).getValues();

  const rowIndex = data.findIndex(row => row[0] === meetingId);
  if (rowIndex !== -1) {
    meetingSheet.getRange(rowIndex + 2, 6).setValue(notes);
    meetingSheet.getRange(rowIndex + 2, 9).setValue(new Date());
  }
}

// Search conversations
function searchConversations(searchTerm, type = null) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const convSheet = ss.getSheetByName(SHEET_NAMES.CONVERSATIONS);
  const data = convSheet.getRange(2, 1, convSheet.getLastRow() - 1, 8).getValues();

  const results = data.filter(row => {
    const contentMatch = row[4].toLowerCase().includes(searchTerm.toLowerCase());
    const typeMatch = type ? row[2] === type : true;
    return contentMatch && typeMatch;
  });

  return results.map(row => ({
    id: row[0],
    meetingId: row[1],
    type: row[2],
    author: row[3],
    content: row[4],
    timestamp: row[5],
    likes: row[6],
    status: row[7]
  }));
}

// Like a conversation
function likeConversation(conversationId) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const convSheet = ss.getSheetByName(SHEET_NAMES.CONVERSATIONS);
  const data = convSheet.getRange(2, 1, convSheet.getLastRow() - 1, 8).getValues();

  const rowIndex = data.findIndex(row => row[0] === conversationId);
  if (rowIndex !== -1) {
    const currentLikes = data[rowIndex][6] || 0;
    convSheet.getRange(rowIndex + 2, 7).setValue(currentLikes + 1);
  }
}

// Include helper to load HTML/CSS files
function include(filename) {
  return HtmlService.createHtmlOutput(HtmlService.createTemplateFromFile(filename).evaluate().getContent());
}
