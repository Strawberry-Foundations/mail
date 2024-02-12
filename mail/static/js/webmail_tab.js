function changeTab(tabId) {
  var tabContents = document.querySelectorAll('.tab-content');

  tabContents.forEach(function(content) {
    content.classList.remove('active-tab');
  });

  var selectedTab = document.getElementById(tabId);
  selectedTab.classList.add('active-tab');
}

function toggleActive(clickedButton) {
  document.querySelectorAll('.sidebar--button').forEach(function(button) {
    button.classList.remove('sidebar--button-active');
  });

  clickedButton.classList.add('sidebar--button-active');
}

function redirectToMailView(mail_id) {
  var urlConstructor = "/webmail/inbox/" + mail_id + "?format=json";
  window.location.href = urlConstructor;
}