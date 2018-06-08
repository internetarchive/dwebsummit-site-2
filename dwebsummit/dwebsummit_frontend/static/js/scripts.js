/**
 * @license AGPL-3
 * @copyright Internet Archive, 2016
 */

$(document).ready(function() {
  $(".js-bio-unit").on('click', function() {
    var bio = $(this).find('.hidden-bio').html();

    var modalEl = document.getElementById('modal');
    if ( ! modalEl) {
      modalEl = document.createElement('div');
      document.body.appendChild(modalEl);
    }
    modalEl.id = 'modal';
    modalEl.className = 'modal';
    modalEl.innerHTML = '';

    var modalInnerEl = document.createElement('div');
    modalInnerEl.className = 'modalInnerEl';

    var bioEl = document.createElement('div');
    bioEl.innerHTML = bio;
    bioEl.className = 'modal-contents';
    modalInnerEl.appendChild(bioEl);

    var prevScrollTop = document.body.scrollTop;

    var closeEl = document.createElement('button');
    closeEl.innerHTML = 'Close';
    closeEl.className = 'close-button';

    var closeDiv = document.createElement('div');
    closeDiv.className = 'close-wrapper';
    closeDiv.appendChild(closeEl);
    modalInnerEl.appendChild(closeDiv);

    modalEl.appendChild(modalInnerEl);
    document.body.style.overflow = 'hidden';
    document.body.style.height = '100%';
    document.body.className += ' open-modal';

    var closeModal = function() {
      document.body.style.overflow = 'auto';
      document.body.style.height = 'auto';
      document.body.className = document.body.className.replace(' open-modal', '');
      document.body.scrollTop = prevScrollTop;
      $(modalEl).remove();
      window.onkeydown = undefined;
    };

    closeEl.onclick = function(e) {
      closeModal();
      e.preventDefault();
    };

    modalEl.onclick = function(e) {
      if (e.target == modalEl) {
        closeModal();
        e.preventDefault();
      }
    };
    window.onkeydown = function(event) {
      if (event.keyCode === 27 /* esc */) {
        closeModal();
      }
    };

  });

  /**
   * Simple carousel effect
   */
  $(".js-carousel").each(function(elem, index) {
    return;
    var currIndex = 0;
    var perPage = 3;
    var msPerPage = 5000;
    var $elem = $(elem);

    var initStyles = function($elem) {
      $elem.children().each(function(child, childIndex) {
        if (childIndex >= (currIndex * perPage) && childIndex < ((currIndex * perPage) + perPage)) {
          child.style.display = 'block';
          child.style.opacity = '1';
        } else {
          child.style.display = 'none';
          child.style.opacity = '0';
        }
      });
    };

    var showIndex = function(nextIndex) {
      var fadeOuts = [];
      var fadeIns = [];
      $elem.children().each(function(child, childIndex) {
        if (childIndex >= (currIndex * perPage) && childIndex < ((currIndex * perPage) + perPage)) {
          fadeIns.push(child);
        } else {
          fadeOuts.push(child);
        }
      });
      $(fadeOuts).each(function(child, childIndex) {
        child.style.transition = 'opacity 2.0s ease-in';
        child.style.opacity = '0';
      });
      setTimeout(function(){
        $(fadeOuts).each(function(child, childIndex) {
          child.style.display = 'none';
        });
        $(fadeIns).each(function(child, childIndex) {
          child.style.display = 'block';
          child.style.transition = 'opacity 1.0s ease-out';
          child.style.opacity = '0';
          setTimeout(function(){
            child.style.opacity = '1';
          }, 50);
        });
      }, 2050);
    };

    initStyles($elem);
    showIndex(currIndex);
    setInterval(function() {
      currIndex = (currIndex + 1) % Math.ceil($elem.children().length / perPage);
      showIndex(currIndex);
    }, msPerPage);
  });
});
