function onStart() {
    fetch('/start_reocrding', {
        method: 'POST'
    }).catch(error => {
        console.error(error);
    });
}

function onStop() {
    fetch('/stop_reocrding', {
        method: 'POST'
    }).catch(error => {
        console.error(error);
    });
}

