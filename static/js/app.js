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
    editor: { line: 0, ch: 0 },
  };


  /*==========  MESH CODE EDITOR BOX  ==========*/

  var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    lineNumbers: true,
    lineWrapping: true,
   // mode: 'python'
  });

//  /*==========  MESH CODE EDITOR BOX  ==========*/
//
//  window.onload = function() {
//    change();
//  };
//
//
//  CodeMirror.modeURL = "../static/js/vendor/%N.js";
//
//  function change() {
//    var val = "{{=filename}}", m, mode, spec;
//    if (m = /.+\.([^.]+)$/.exec(val)) {
//      var info = CodeMirror.findModeByExtension(m[1]);
//      if (info) {
//        mode = info.mode;
//        spec = info.mime;
//      }
//    } else if (/\//.test(val)) {
//      var info = CodeMirror.findModeByMIME(val);
//      if (info) {
//        mode = info.mode;
//        spec = val;
//      }
//    } else {
//      mode = spec = val;
//    }
//    if (mode) {
//      editor.setOption("mode", spec);
//      CodeMirror.autoLoadMode(editor, mode);
//      document.getElementById("modeinfo").textContent = spec;
//    } else {
//      alert("Could not find a mode corresponding to " + val);
//    }
//}



  /*==========  FIREBASE DATA FETCHING  ==========*/

  var notifyFireBase = true;

  appRef.on('value', function(snapshot) {
    var content = snapshot.val();
    notifyFireBase = true;

    editor.setCursor({
      line: position.editor.line,
      ch: position.editor.ch
    });
  });


  /*==========  CODE EVENT LISTENERS  ==========*/

  var sync = function() {
    var editorContent = editor.getValue();

    position.editor   = editor.getCursor();

    appRef.set({
      editor: {
        text: editorContent
      },
    });
  };

  editor.on('change', function() {
   updatePreview();
    if (notifyFireBase) sync();
  });


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
