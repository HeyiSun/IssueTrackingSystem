var global = {};
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function changeStatus() {
    const issue_id = getParameterByName("issue_id");
    var to_status_target = event.target;
    const to_status_name = to_status_target.innerText || to_status_target.textContent;
    const url = `/status_change/?issue_id=${issue_id}&to_status_name=${to_status_name}`;
    window.location.href = url;
}

function addIssue() {
    const project_id = getParameterByName("project_id");
    const url = `/issue_add/?project_id=${project_id}`;
    window.location.href = url;
}

function focusOut() {
    let box_element = document.getElementById("invisible box");
    let button_element = document.getElementById("popup button");
    let icon_element = button_element.getElementsByTagName('span')[0];

    global['timer'] = setTimeout(function () {
        if (box_element.classList.contains("visible")) {
            box_element.classList.remove("visible");
            box_element.classList.add("invisible");
        }
        if (icon_element.classList.contains("fa-check")) {
            icon_element.classList.remove('fa-check');
            icon_element.classList.toggle('fa-plus');
        }
    }, 0);
}

function focusIn() {
    clearTimeout(global['timer']);
}

function pressPlusButton() {
    let button_element = document.getElementById("popup button");
    let box_element = document.getElementById("invisible box");
    let icon_element = button_element.getElementsByTagName('span')[0];
    const dest = button_element.getAttribute('dest');

    if (icon_element.classList.contains("fa-plus")) {
        console.log("plus");
        icon_element.classList.remove('fa-plus');
        icon_element.classList.add('fa-check');
    } else {
        console.log(dest);
        if (dest == '/lead/') {
            const project_id = getParameterByName("project_id");
            const new_leader_username = box_element.value;
            const url = `${dest}?project_id=${project_id}&new_leader_username=${new_leader_username}`;
            window.location.href = url;
        } else if (dest == '/assign/') {
            const issue_id = getParameterByName("issue_id");
            const assignee_username = box_element.value;
            const url = `${dest}?issue_id=${issue_id}&assignee_username=${assignee_username}`;
            window.location.href = url;
        }
    }

    if (box_element.classList.contains("invisible")) {
        box_element.classList.remove("invisible");
        box_element.classList.add("visible");
        box_element.focus();
    }
}
