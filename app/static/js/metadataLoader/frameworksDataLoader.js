import {buildBaseUi} from "../selectFromFrameworks/baseUi.js";


export function loadFrameworksData(group, inputData) {
    const container = document.getElementById(`${group}-container`);

    for (const box of container.getElementsByClassName(`${group}-box`)){
        box.remove();
    }

    inputData = inputData[group];

    for (let i = 0; i < inputData.length; i++){  // for loop with counter because value and index is needed
        if(i === 0){
            buildBaseUi(group);
        } else {
            buildBaseUi(group, false);
        }

        const boxes = container.getElementsByClassName(`${group}-box`);
        const subContainer = boxes[boxes.length - 1];

        const framework = inputData[i]["educationalFramework"];
        const name = inputData[i]["name"][0]["name"];  // Always first item from Name object -> change to
        // look for "en", then "de", then first?
        const uri = inputData[i]["targetUrl"];

        const selectionStorage = subContainer.getElementsByClassName(`selected-${group}`)[0];

        selectionStorage.textContent = `${name}@${framework}`;
        selectionStorage.setAttribute('targetUrl', uri);
    }
}
