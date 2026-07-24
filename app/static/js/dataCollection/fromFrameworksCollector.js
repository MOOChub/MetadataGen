import {isEmpty} from "../dataCheck/checkHelper.js";


export function collectFrameworkData(data, group) {
    const container = document.getElementById(`${group}-container`);
    const boxes = container.getElementsByClassName(`${group}-box`);

    const dataFragments = [];
    let suggestionFramework = null;  // for generating suggestion if no entry is selected

    for (const box of boxes){
        const inputs = box.getElementsByClassName(`selected-${group}`);
        let dataFragment = {};

        for (const input of inputs){
            const selected = input.textContent;
            const name = selected.split("@")[0];

            if(name === "None selected"){
                suggestionFramework = box.getElementsByClassName(`select-framework-${group}`)[0].value
                continue;
            }

            const framework = selected.split("@")[1];
            let uri = input.getAttribute('targetUrl');

            dataFragment = {
                "name": name,
                "educationalFramework": framework
            }
            if(uri){
                dataFragment["targetUrl"] = uri;
            }
        }
        if(!isEmpty(dataFragment)){
            dataFragments.push(dataFragment);
        }
    }
    if(!isEmpty(dataFragments)){
        data[group] = dataFragments;
    } else {
        data[group] = [{"educationalFramework": suggestionFramework}];
    }
}