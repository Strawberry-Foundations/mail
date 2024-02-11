function change_tab(tabId) {
  var tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(function(content) {
    content.classList.remove('active-tab');
  });

  var selectedTab = document.getElementById(tabId);
  selectedTab.classList.add('active-tab');
}