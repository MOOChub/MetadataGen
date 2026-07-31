import {buildRow} from "../helper.js";
import {getSubEntries} from "./frameworkDataHandler.js";


export function buildFrameworkSelect(frameworks, container, group) {
    const frameworkSelect = document.createElement('select');
    frameworkSelect.id = `${group}-select-${crypto.randomUUID()}`;
    frameworkSelect.className = `select-framework-${group}`;

    for (const key of Object.keys(frameworks)){
        const option = document.createElement('option');
        option.textContent = key;
        option.value = key;

        frameworkSelect.appendChild(option);
    }

    container.appendChild(buildRow(frameworkSelect, "framework", false));

    let frameworkName = frameworkSelect.value;
    let selectedFramework = frameworks[frameworkName];
    const accordionContainer = document.createElement('div');

    const selectionStorage = document.createElement('p');
    selectionStorage.id = `selected-${crypto.randomUUID()}`;
    selectionStorage.className = `selected-${group}`;
    selectionStorage.textContent = "None selected";

    buildEntries(accordionContainer, group, frameworkName, selectedFramework, selectionStorage);

    frameworkSelect.onchange = function () {
        for (const c of accordionContainer.children) {
            c.remove();
        }
        frameworkName = frameworkSelect.value;
        selectedFramework = frameworks[frameworkName];
        buildEntries(accordionContainer, group, frameworkName, selectedFramework,selectionStorage);
    }

    const row = buildRow(accordionContainer, `Select ${group}`,false, 6);
    container.appendChild(row);

    container.appendChild(buildRow(selectionStorage, "Selected", false));
}


function buildEntries(container, group, framework, entries, selectionStorage) {
    const subContainer = document.createElement('div');
    subContainer.className = 'accordion';
    subContainer.id = `accordion-${crypto.randomUUID()}`;

    for(const entry of entries){
        const name = entry["name"];
        const uri = entry["uri"];

        if(entry["hasNarrower"]){
            const item = document.createElement('div');
            item.className = 'accordion-item';

            const header = document.createElement('h2');
            header.className = 'accordion-header';

            const btn = document.createElement('button');
            btn.className = "accordion-button collapsed";
            btn.textContent = name;

            btn.setAttribute("data-bs-toggle", "collapse");
            header.appendChild(btn);

            item.appendChild(header);

            const collapse = document.createElement('div');
            collapse.className = "accordion-collapse collapse";
            collapse.id = `collapse-${crypto.randomUUID()}`;

            btn.setAttribute("data-bs-target", `#${collapse.id}`);
            btn.setAttribute("aria-expanded", "false");
            btn.setAttribute("aria-controls", collapse.id);

            collapse.setAttribute("aria-labelledby", collapse.id);
            collapse.setAttribute("data-bs-parent", subContainer.id);

            btn.onclick = async function (){
                const subEntries = await getSubEntries(group, framework, uri);

                if(subEntries.length > 0 && collapse.children.length === 0){
                    const body = document.createElement('div');
                    body.className = "accordion-body";

                    buildEntries(body, group, framework, subEntries, selectionStorage);
                    collapse.appendChild(body);
                }
            }

            const selectBtn = buildSelectButton(framework, name, uri, selectionStorage);
            const p = document.createElement('p');
            p.setAttribute('align', 'right');
            p.appendChild(selectBtn);
            item.appendChild(p);

            item.appendChild(collapse);

            subContainer.appendChild(item);
        } else {
            const btn = buildSelectButton(framework, name, uri, selectionStorage);

            const row = buildRow(btn, name, false);
            subContainer.appendChild(row);
        }
    }
    container.appendChild(subContainer);
}


function buildSelectButton(framework, name, uri, selectionStorage) {
    const selectBtn = document.createElement('button');
    selectBtn.textContent = 'Select';
    selectBtn.setAttribute('style', "float:right;");
    selectBtn.onclick = function () {
        selectionStorage.textContent = `${name}@${framework}`;
        selectionStorage.setAttribute('targetUrl', uri);
    }
    return selectBtn
}