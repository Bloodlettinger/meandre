/*
*   Upload files to the server using HTML 5 Drag and drop the folders on your local computer
*
*   Tested on:
*   Mozilla Firefox 3.6.12
*   Google Chrome 7.0.517.41
*   Safari 5.0.2
*   WebKit r70732
*
*   The current version does not work on:
*   Opera 10.63
*   Opera 11 alpha
*   IE 6+
*/

function uploader(place, status, url, onload_handler, position_handler, tag_list) {
    var tag_list = tag_list || false;  // empty string is a default value

    var get_url = function(base64) {
        var base64 = base64||false;
        var delim = '';
        var opts = '?';
        if (base64)
            opts += delim + 'base64=true';
            delim = '&';
        if (tag_list)
            opts += delim + 'tags=' + tag_list;
            delim = '&';
        if (typeof position_handler == 'function')
            opts += delim + 'position=' + position_handler();
            delim = '&';
        return url + opts;
    }

    // Upload image files
    var upload = function(file) {
        // Firefox 3.6, Chrome 6, WebKit
        if(window.FileReader) {

            // Once the process of reading file
            this.loadEnd = function() {
                var bin = reader.result;
                var xhr = new XMLHttpRequest();
                var url = get_url(xhr.sendAsBinary == null);
                xhr.open('POST', url , true);
                var boundary = 'xxxxxxxxx';
                var body = '--' + boundary + "\r\n";
                body += 'Content-Disposition: form-data; name="upload"; filename="' + file.name + '"\r\n';
                body += "Content-Type: application/octet-stream\r\n\r\n";
                body += bin + "\r\n";
                body += '--' + boundary + '--';
                xhr.setRequestHeader('content-type', 'multipart/form-data; boundary=' + boundary);

                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4) {
                        if(xhr.status == 200) {
                            onload_handler(xhr.responseText);
                        }
                    }
                };

                if(xhr.sendAsBinary != null) {
                    // Firefox 3.6 provides a feature sendAsBinary ()
                    xhr.sendAsBinary(body);
                } else {
                    // Chrome 7 sends data but you must use the base64_decode on the server side
                    xhr.setRequestHeader('UP-FILENAME', file.name);
                    xhr.setRequestHeader('UP-SIZE', file.size);
                    xhr.setRequestHeader('UP-TYPE', file.type);
                    xhr.send(window.btoa(bin));
                }
                if (status) {
                    var div = document.getElementById(status);
                    div.innerHTML = 'Sent : 100%';
                }
            }

            // Loading errors
            this.loadError = function(event) {
                switch(event.target.error.code) {
                    case event.target.error.NOT_FOUND_ERR:
                        document.getElementById(status).innerHTML = 'File not found!';
                    break;
                    case event.target.error.NOT_READABLE_ERR:
                        document.getElementById(status).innerHTML = 'File not readable!';
                    break;
                    case event.target.error.ABORT_ERR:
                    break;
                    default:
                        document.getElementById(status).innerHTML = 'Read error.';
                }
            }

            // Reading Progress
            this.loadProgress = function(event) {
                if (event.lengthComputable) {
                    var percentage = Math.round((event.loaded * 100) / event.total);
                    document.getElementById(status).innerHTML = 'Loaded : '+percentage+'%';
                }
            }

            var reader = new FileReader();
            if(reader.addEventListener) {
                // Firefox 3.6, WebKit
                reader.addEventListener('loadend', this.loadEnd, false);
                if (status != null)
                {
                    reader.addEventListener('error', this.loadError, false);
                    reader.addEventListener('progress', this.loadProgress, false);
                }
            } else {
                // Chrome 7
                reader.onloadend = this.loadEnd;
                if (status != null)
                {
                    reader.onerror = this.loadError;
                    reader.onprogress = this.loadProgress;
                }
            }

            // The function that starts reading the file as a binary string
            reader.readAsBinaryString(file);
        } else {
            // Safari 5 does not support FileReader
            var xhr = new XMLHttpRequest();
            xhr.open('POST', get_url(), true);
            xhr.setRequestHeader('UP-FILENAME', file.name);
            xhr.setRequestHeader('UP-SIZE', file.size);
            xhr.setRequestHeader('UP-TYPE', file.type);
            xhr.send(file);

            if (status) {
                document.getElementById(status).innerHTML = 'Loaded : 100%';
            }
        }
    }

    var noopHandler = function(event) {
        event.stopPropagation();
        event.preventDefault();
    }

    var dropHandler = function(event) {
        noopHandler(event);
        var dt = event.dataTransfer;
        var files = dt.files;
        for (var i = 0; i<files.length; i++) {
            upload(files[i]);
        }
    }

    // The inclusion of the event listeners (DragOver and drop)
    this.uploadPlace =  document.getElementById(place);
    this.uploadPlace.addEventListener("dragover", noopHandler, true);
    this.uploadPlace.addEventListener("drop", dropHandler, false);
}
