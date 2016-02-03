// This code was adapted from code written by Farhad Ghayour,
// github repo at https://github.com/FarhadG/mesh-code-editor


$(function() {

  var $window = $(window);
  // TODO(Ckyle): Firebase seems to be sometype of database host,
  // We should try to get off of the mesh-editor's account
  // ASAP
  var appRef = new Firebase('https://mesh-editor.firebaseio.com/');

  /*==========  User's Cursor  ==========*/

  var position = {
    html: { line: 0, ch: 0 },
  };


  /*==========  MESH CODE EDITOR BOXES  ==========*/

  var htmlBox = CodeMirror.fromTextArea(document.getElementById('html'), {
    lineNumbers: true,
    lineWrapping: true,
    mode: 'python'
  });

  /*==========  FIREBASE DATA FETCHING  ==========*/

  var notifyFireBase = true;

  appRef.on('value', function(snapshot) {
    var content = snapshot.val();
    notifyFireBase = true;

    htmlBox.setCursor({
      line: position.html.line,
      ch: position.html.ch
    });
  });


  /*==========  CODE EVENT LISTENERS  ==========*/

  var sync = function() {
    var htmlContent = htmlBox.getValue();

    position.html   = htmlBox.getCursor();

    appRef.set({
      html: {
        text: htmlContent
      },
    });
  };

  htmlBox.on('change', function() {
   updatePreview();
    if (notifyFireBase) sync();
  });


  /*==========  PREVIEW UPDATING  ==========*/

//  var delay;
//  var updatePreview = function() {
//    clearTimeout(delay);
//
//    var update = function() {
//      var previewFrame = document.getElementById('preview');
//      var preview =  previewFrame.contentDocument ||  previewFrame.contentWindow.document;
//      preview.open();
//      preview.write(getContent());
//      preview.close();
//    };
//
//    delay = setTimeout(update, 500);
//  }
//
//  setInterval(updatePreview, 1000);
//
//
  /*==========  STYLING & DYNAMIC BOX SIZING  ==========*/

  $('.lights').click(function(el) {
    el.preventDefault();
    $('.cm-s-default').toggleClass('cm-s-monokai');
    $(this).toggleClass('button-on');
  }).click();

  $('.together').click(function(el) {
    el.preventDefault();
    $(this).toggleClass('button-on');
  }).click();

  $('#frame').animate({
    'height': ($window.height() / 1.8),
    'width': ($window.width() / 2)
  }, 1000);

  var resizeBoxes = function() {
    var windowHeight = $(window).height();
    var windowWidth  = $(window).width();
    $textBoxes = $('.CodeMirror');
    $.each($textBoxes, function(idx, box) {
      $(box).height(windowHeight / 2.2);
      $(box).width(windowWidth / 2.15);
    });
  };

  resizeBoxes();

  $window.resize(function() {
    resizeBoxes();
  });

  $('#frame').draggable().resizable({
    handles: 'n, e, s, w, ne, se, sw, nw'
  });

});
