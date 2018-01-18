(function () {
    var session;

    function receiverListener(e) {
        if (e === chrome.cast.ReceiverAvailability.AVAILABLE) {
            console.log("onReceiver available");
        }
    }

    function sessionListener(e) {
        session = e;
        if (session.media.length != 0) {
            console.log('onRequestSessionSuccess', session.media[0]);
        }
    }

    var initializeCastApi = function () {
        var onInitSuccess = function (a) {
            console.log("onInitSuccess", a);
        };
        var onError = function (a) {
            console.log("onInitError", a);
        };
        var sessionRequest = new chrome.cast.SessionRequest(chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID);
        var apiConfig = new chrome.cast.ApiConfig(sessionRequest, sessionListener, receiverListener);
        chrome.cast.initialize(apiConfig, onInitSuccess, onError);
    };

    window['__onGCastApiAvailable'] = function (loaded, errorInfo) {
        if (loaded) {
            initializeCastApi();
            console.log("Google cast api available");
        } else {
            console.log("Error while initializing google cast", errorInfo);
        }
    };

    window['sendMediaOnGoogleCast'] = function (url) {
        console.log("sendMediaOnGoogleCast", url);
        if (typeof chrome === 'undefined' || !chrome || !chrome.cast) {
            alert('Google cast is unavailable');
            return false;
        }

        chrome.cast.requestSession(function (r) {
            var d;
            var deviceName = (d = r).receiver.friendlyName;
            console.log("Playing on device " + deviceName);

            var mediaInfo = new chrome.cast.media.MediaInfo(url),
                o = new chrome.cast.media.LoadRequest(mediaInfo);

            console.log(mediaInfo, o);
            d.loadMedia(o, function (r) {
                console.log("Load media", r);
                r.addUpdateListener(function (n) {
                    if (d) {
                        var a = r.playerState;
                        console.log("newPlayerState", a);
                    }
                })
            }, function (e) {
                console.error("load media error", e);
            });
        }, function (e) {
            console.error("requestSession error", e)
        });
        return false;
    };
})();
