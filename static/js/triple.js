var throttle = false;
var flipped = false;

document.querySelector('div#pic').addEventListener('click', function (evt) {
    var o = this,
        ot = this.textContent;

    if (!throttle && evt.detail === 2) {

        if (!flipped) {
            document.getElementById('pic').style.backgroundImage="url('static/img/triple.jpg')";
            flipped = true;
        } else {
            if (window.devicePixelRatio === 1){
                document.getElementById('pic').style.backgroundImage="url('static/img/me@1x.jpg')";
            } else if (window.devicePixelRatio === 2) {
                document.getElementById('pic').style.backgroundImage="url('static/img/me@2x.jpg')";
            } else {
                document.getElementById('pic').style.backgroundImage="url('static/img/me@3x.jpg')";
            }
            flipped = false;
        }

        throttle = true;
        setTimeout(function () {
            o.textContent = ot;
            throttle = false;
        }, 500);
    }
});
