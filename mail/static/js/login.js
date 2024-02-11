function unfocus(element) {
  document.getElementById(element).addEventListener('blur', function() {
    this.classList.add('input-field--unfocus');
  });  
}
