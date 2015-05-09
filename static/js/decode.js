function decodeURL( str ) {
  var decoded = decodeURIComponent(escape(window.atob( str )));
  window.location.href = decoded
}
