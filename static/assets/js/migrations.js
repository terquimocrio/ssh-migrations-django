let projectSelect = document.getElementById('id_project');
let branchSelect = document.getElementById('id_branches');

projectSelect.addEventListener('change', e => {
    let projectId = e.target.value;
    let projectsResult = null
    let defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.text = 'Select branch';
    defaultOption.selected = true;
    fetch(`/api/get_branches/${projectId}`).then(response => response.json()).then(data => {

        projectsResult = data;
        branchSelect.innerHTML = '';

        branchSelect.appendChild(defaultOption);

        projectsResult.forEach(project => {
            let option = document.createElement('option');
            option.value = project.name;
            option.text = project.name;
            branchSelect.appendChild(option);
        });
    }).catch(error => {
        branchSelect.innerHTML = '';
        branchSelect.appendChild(defaultOption);
    });    
});

