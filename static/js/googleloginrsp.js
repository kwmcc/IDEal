var auth2 = gapi.auth2.init();

auth2.then(function () {
    if (auth2.isSignedIn.get()) {
        window.location="http://localhost:8000/IDEal/default/ideal_editor.html"
    }
});
