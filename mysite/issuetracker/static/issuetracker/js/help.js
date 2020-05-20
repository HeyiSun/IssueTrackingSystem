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
